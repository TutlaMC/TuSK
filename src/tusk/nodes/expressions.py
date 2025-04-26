from tusk.node import Node
from tusk.token import Token
from tusk.variable import *
from tusk.nodes.base.name import NameNode

class FactorNode(Node):
    def __init__(self, value:Token, rules=[]):
        super().__init__("1n", "FactorNode", [value], auto_eval=True)
        self.interpreter = value.interpreter
        self.rules = rules

        self.value = value
        self.orginal_token = value
        self.auto_eval = True

        self.type = "1n"
        

        if self.value.type == "NUMBER":
            self.value = float(self.value.value)
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
                    self.value = get_type_(self.interpreter.next_token())
            

                        
        elif self.value.type == "EFFECT":
            if self.value.value == "input":
                from tusk.nodes.effects.input_ import InputNode
                self.value = InputNode(self.value).value
            elif self.value.value == "convert":
                from tusk.nodes.effects.types_ import ConvertNode
                self.value = ConvertNode(self.value).value
            elif self.value.value == "add":
                from tusk.nodes.effects.string_list_common import AddNode
                self.value = AddNode(self.value).value
            elif self.value.value == "remove":
                from tusk.nodes.effects.string_list_common import RemoveNode
                self.value = RemoveNode(self.value).value
            elif self.value.value == "replace":
                from tusk.nodes.effects.string_list_common import ReplaceNode
                self.value = ReplaceNode(self.value).value
            elif self.value.value == "length":
                from tusk.nodes.effects.string_list_common import LengthNode
                self.value = LengthNode(self.value).value
            elif self.value.value == "split":
                from tusk.nodes.effects.string_list_common import SplitNode
                self.value = SplitNode(self.value).value
            elif self.value.value == "shell":
                from tusk.nodes.effects.exec_ import ShellNode
                self.value = ShellNode(self.value).value
        elif self.value.type == "IDENTIFIER":
            if is_ordinal_number(self.value):
                n = is_ordinal_number(value)-1
                self.interpreter.expect_token("KEYWORD:character|KEYWORD:item")
                self.interpreter.expect_token("LOGIC:in")
                list_ = ExpressionNode(self.interpreter.next_token()).value
                self.value = list_[n]
                
            elif self.value.value in self.value.interpreter.data["vars"]:
                self.value = NameNode(self.value).value
            elif self.value.value in self.value.interpreter.data["funcs"]: # calls function
                
                func = self.value.interpreter.data["funcs"][self.value.value] # [[], interpreter]
                func_name= self.value.value
                func_interpreter = func[1]
                parased_params = []
                if len(func[0]) > 0: # length of params, function doesnt need params
                    for param in func[0]: # looping params (func[0] is the param list)
                        e = self.interpreter.next_token() # next token, the code afer this checks if it matches the required param
                        node = ExpressionNode(e)
                        if len(param.split(":")) > 1:
                            if get_type_(node.value) == param.split(":")[0].upper():
                                parased_params.append([param.split(":")[1],node.value])
                            else:
                                raise Exception(f"Recieved type {get_type_(ExpressionNode(e))} instead of {param.split(':')[0]} in function {self.value.value} ") 
                        else:
                            parased_params.append([param,node.value])
                for i in parased_params: func_interpreter.data["vars"][i[0]] = i[1]
                self.value = func_interpreter.compile()

            else: raise Exception(f"Undefined variable {self.value.value}")
        elif self.value.type == "LEFT_CURLY":
            dct = {}
            while self.interpreter.get_next_token().type != "RIGHT_CURLY":
                e = self.interpreter.next_token()
                if e.type in ["STRING"]:
                    key = e.value
                    self.interpreter.expect_token("COLON")
                    value = ExpressionNode(self.interpreter.next_token(), rules=["noLists"]).value
                    dct[key] = value
                if self.interpreter.get_next_token().type == "COMMA":
                    self.interpreter.next_token()
            self.interpreter.expect_token("RIGHT_CURLY")
            self.value = dct
        elif self.value.type == "LEFT_PAR":
            self.value = ExpressionNode(self.interpreter.next_token()).value
            self.interpreter.next_token()
        else:
            raise Exception(f"Invalid factor node type {value}")

        # Lists
        if not "noLists" in self.rules:
            list_ = [self.value]

            while self.interpreter.get_next_token().type == "COMMA":
                self.interpreter.next_token()
                list_.append(ExpressionNode(self.interpreter.next_token(),rules=["noLists"]).value)
            if len(list_) > 1: self.value = list_
         
class TermNode(Node):
    def __init__(self, factor:Token,rules=[]):
        self.auto_eval = True
        self.interpreter = factor.interpreter
        self.rules = rules
        
        
        tkn1 = FactorNode(factor,rules=self.rules)
        if self.interpreter.get_next_token().type == "OPERATOR":
            operator = self.interpreter.get_next_token()
            if operator.value in ["*","/","**","^"]:
                operator = self.interpreter.next_token()
                tkn2 = ExpressionNode(self.interpreter.next_token())
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

class ExpressionNode(Node):
    def __init__(self, token:Token,rules=[]):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.rules = rules


        if token.type=="OPERATOR" and token.value == "-": # Negative Numbers
            if self.interpreter.get_next_token().type=="NUMBER": 
                e = self.interpreter.next_token().value
                self.interpreter.current_token = Token("NUMBER",int(token.value+e),self.interpreter)
                token = self.interpreter.current_token

        tkn1 = TermNode(token,rules=rules)
        if token.interpreter.get_next_token().type in ["OPERATOR", "COMPARISION"]:
            operator = self.interpreter.next_token()
            tkn2 = ExpressionNode(self.interpreter.next_token(),rules=rules)
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