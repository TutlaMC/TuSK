from tusk.node import Node
from tusk.token import Token
from tusk.variable import *
from tusk.nodes.base.name import NameNode
from tusk.nodes.base.function import ExecuteFunctionNode

import asyncio
class FactorNode(Node):
    def __init__(self, value:Token, rules=[]):
        super().__init__("1n", "FactorNode", [value], auto_eval=True)
        self.interpreter = value.interpreter
        self.rules = rules

        self.value = value
        self.orginal_token = value
        self.auto_eval = True
        self.returned_var = None

        self.type = "1n"

    async def create(self):
        self.interpreter.debug_msg(self.value, "<- factor (node) start")
        if self.value.type == "NUMBER":
            if "." in self.value.value:
                self.value = float(self.value.value)
            else:
                self.value = int(self.value.value)
            if self.interpreter.get_next_token().type == "TIME":
                time_key = {
                    "milisecond": 0.001,
                    "second": 1,
                    "minute": 60,
                    "hour": 3600,
                    "day": 86400,
                    "week": 604800,
                    "month": 2592000,
                    "year": 31536000
                }
                
                e = self.interpreter.next_token()
                self.value = self.value * time_key[e.value]
        elif self.value.type == "STRING":
            self.value = str(self.value.value)
        elif self.value.type == "BOOL":
            if self.value.value == "true": self.value = True
            else: self.value = False
        elif self.value.type == "TYPE":
            self.value = types_[self.value.value]
        elif self.value.type == "NOTHING":
            self.value = None
        elif self.value.type == "KEYWORD":
            if self.value.value == "what":
                nxt_tkn = self.interpreter.next_token()
                if nxt_tkn.type=="KEYWORD" and nxt_tkn.value == "type":
                    self.interpreter.expect_token("COMPARISION:is")
                    self.value = await get_type_(self.interpreter.next_token())
            elif self.value.value == "get":
                from tusk.nodes.effects.get_ import GetNode
                self.value = (await GetNode(self.value).create()).value
                        
        elif self.value.type == "EFFECT":
            if self.value.value == "input":
                from tusk.nodes.effects.input_ import InputNode
                self.value = (await InputNode(self.value).create()).value
            elif self.value.value == "convert":
                from tusk.nodes.effects.types_ import ConvertNode
                self.value = (await ConvertNode(self.value).create()).value
            elif self.value.value == "add":
                from tusk.nodes.effects.string_list_common import AddNode
                self.value = (await AddNode(self.value).create()).value
            elif self.value.value == "remove":
                from tusk.nodes.effects.string_list_common import RemoveNode
                self.value = (await RemoveNode(self.value).create()).value
            elif self.value.value == "replace":
                from tusk.nodes.effects.string_list_common import ReplaceNode
                self.value = (await ReplaceNode(self.value).create()).value
            elif self.value.value == "length":
                from tusk.nodes.effects.string_list_common import LengthNode
                self.value = (await LengthNode(self.value).create()).value
            elif self.value.value == "split":
                from tusk.nodes.effects.string_list_common import SplitNode
                self.value = (await SplitNode(self.value).create()).value
            elif self.value.value == "index":
                from tusk.nodes.effects.string_list_common import IndexNode
                self.value = (await IndexNode(self.value).create()).value
            elif self.value.value == "shell":
                from tusk.nodes.effects.exec_ import ShellNode
                self.value = (await ShellNode(self.value).create()).value
            elif self.value.value == "python":
                from tusk.nodes.effects.exec_ import PythonNode
                self.value = (await PythonNode(self.value).create()).value
            elif self.value.value == "request":
                from tusk.nodes.effects.requests_ import RequestNode
                self.value = (await RequestNode(self.value).create()).value
            elif self.value.value == "read":
                from tusk.nodes.effects.fs import ReadNode
                self.value = (await ReadNode(self.value).create()).value

            ### DISCORD EFFECTS
            elif self.value.value == "send":
                from tusk.nodes.discord.effects.send import SendNode
                self.value = (await SendNode(self.value).create()).value
                
                
        elif self.value.type == "IDENTIFIER":
            ordn = is_ordinal_number(self.value)
            if self.value.value == "response":print(self.value.value, self.value.interpreter.data["vars"][self.value.value])
            if ordn:
                n = ordn-1
                self.interpreter.expect_token("KEYWORD:character|KEYWORD:item")
                self.interpreter.expect_token("LOGIC:in")
                list_ = (await FactorNode(self.interpreter.next_token()).create()).value
                self.value = list_[n]
                
            elif self.value.value in self.value.interpreter.data["vars"]:
                self.value = (await NameNode(self.value).create()).value
            elif self.value.value in self.value.interpreter.data["funcs"]: # calls function
                self.value = (await ExecuteFunctionNode(self.value).create()).value
                

            else: self.interpreter.error("Undefined variable", f"Undefined variable {self.value.value}")
        elif self.value.type == "LEFT_CURLY":
            dct = {}
            while self.interpreter.get_next_token().type != "RIGHT_CURLY":
                e = self.interpreter.next_token()
                if e.type in ["STRING"]:
                    key = e.value
                    self.interpreter.expect_token("COLON")
                    value = (await ExpressionNode(self.interpreter.next_token(), rules=["noLists"]).create()).value
                    dct[key] = value
                if self.interpreter.get_next_token().type == "COMMA":
                    self.interpreter.next_token()
            self.interpreter.expect_token("RIGHT_CURLY")
            self.value = dct
        elif self.value.type == "LEFT_PAR":
            self.value = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.interpreter.next_token()
        else:
            raise Exception(f"Invalid factor node type {value}")

        # Lists
        if not "noLists" in self.rules:
            list_ = [self.value]

            while self.interpreter.get_next_token().type == "COMMA":
                self.interpreter.next_token()
                list_.append((await ExpressionNode(self.interpreter.next_token(),rules=["noLists"]).create()).value)
            if len(list_) > 1: self.value = list_
        self.interpreter.debug_msg("factor", "<- factor (node) end")
        return self
class TermNode(Node):
    def __init__(self, factor:Token,rules=[]):
        self.auto_eval = True
        self.interpreter = factor.interpreter
        self.rules = rules
        self.returned_var = None
        
        self.factor = factor

    async def create(self):
        self.interpreter.debug_msg(self.factor, "<- term (node) start")
        tkn1 = await FactorNode(self.factor,rules=self.rules).create()
        
        if self.interpreter.get_next_token().type == "OPERATOR":
            operator = self.interpreter.get_next_token()
            if operator.value in ["*","/","**","^"]:
                operator = self.interpreter.next_token()
                tkn2 = await ExpressionNode(self.interpreter.next_token()).create()
                if operator.value == "*":
                    self.value = tkn1.value * tkn2.value
                elif operator.value == "/":
                    self.value = tkn1.value / tkn2.value
                elif operator.value == "^":
                    self.value = int(tkn1.value)^int(tkn2.value)
            else:
                self.value = tkn1.value
        else:
            self.value = tkn1.value
        self.interpreter.debug_msg("term", "<- term (node) end")
        return self

class ExpressionNode(Node):
    def __init__(self, token:Token,rules=[]):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.rules = rules
        self.returned_var = None
        self.token = token

    async def create(self):
        self.interpreter.debug_msg(self.token, "<- expr (node) start")
        if self.token.type=="OPERATOR" and self.token.value == "-": # Negative Numbers
            if self.interpreter.get_next_token().type=="NUMBER": 
                e = self.interpreter.next_token().value
                self.interpreter.current_token = Token("NUMBER",int(self.token.value+e),self.interpreter)
                self.token = self.interpreter.current_token

        tkn1 = await TermNode(self.token,rules=self.rules).create()
        if self.token.interpreter.get_next_token().type in ["OPERATOR", "COMPARISION"]:
            operator = self.interpreter.next_token()
            tkn2 = await ExpressionNode(self.interpreter.next_token(),rules=self.rules).create()
            if operator.type == "OPERATOR":
                if operator.value == "+":
                    self.value = tkn1.value + tkn2.value
                elif operator.value == "-":
                    self.value = tkn1.value - tkn2.value
            elif operator.type == "COMPARISION":
                if operator.value == "<":
                    self.value = tkn1.value < tkn2.value
                elif operator.value == ">":
                    self.value = tkn1.value > tkn2.value
                elif operator.value == "<=":
                    self.value = tkn1.value <= tkn2.value
                elif operator.value == ">=":
                    self.value = tkn1.value >= tkn2.value
                elif operator.value == "==":
                    self.value = tkn1.value == tkn2.value
                elif operator.value == "is":
                    self.value = tkn1.value == tkn2.value
                elif operator.value == "!=":
                    self.value = tkn1.value != tkn2.value
            self.type="3en"
        else:
            self.value = tkn1.value
            self.type="1en"
        self.interpreter.debug_msg(self.interpreter.current_token, "<- expr (node) end")
        return self