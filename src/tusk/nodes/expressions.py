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
        elif self.value.type == "STRING":
            self.value = str(self.value.value)
        elif self.value.type == "BOOL":
            if self.value.value == "true": self.value = True
            else: self.value = False
        elif self.value.type == "TYPE":
            self.value = types_[self.value.value]
        elif self.value.type == "KEYWORD":
            if self.value.value == "what":
                nxt_tkn = self.interpreter.next_token()
                if nxt_tkn.type=="KEYWORD" and nxt_tkn.value == "type":
                    self.interpreter.expect_token("COMPARISION:is")
                    self.value = get_type_(self.interpreter.next_token())
            elif self.value.value == "input":
                self.value = input(ExpressionNode(self.interpreter.next_token()).value)
            elif self.value.value == "convert":
                val = ExpressionNode(self.interpreter.next_token()).value
                self.interpreter.expect_token("KEYWORD:to")
                self.value = types_[self.interpreter.next_token().value](val)
            
            elif self.value.value == "add":
                item = ExpressionNode(self.interpreter.next_token()).value
                self.interpreter.expect_token("KEYWORD:to")
                list_ = ExpressionNode(self.interpreter.next_token()).value
                if type(list_) != list: 
                    self.value = item+list_
                else:
                    list_.append(item)
                    self.value = list_
            elif self.value.value == "remove":
                item = is_ordinal_number(self.interpreter.next_token())
                self.interpreter.expect_token("KEYWORD:item")
                if item:
                    item-=1
                    self.interpreter.expect_token("KEYWORD:from")
                    list_ = ExpressionNode(self.interpreter.next_token()).value
                    if type(list_) != list: 
                        raise Exception(f"remove requires <list> not {type(list_)}")
                    else:
                        list_.pop(item)
                        self.value = list_
                else: raise Exception(f"remove expected ordinal number not {self.interpreter.current_token.value}, cardinal numbers are 1st, 2nd, 3rd, 4th, 5th...")
            elif self.value.value == "replace":
                to_replace = str(ExpressionNode(self.interpreter.next_token()).value)
                self.interpreter.expect_token("KEYWORD:with")
                with_replace = str(ExpressionNode(self.interpreter.next_token()).value)
                self.interpreter.expect_token("LOGIC:in")
                self.value = str(ExpressionNode(self.interpreter.next_token()).value).replace(to_replace,with_replace)
            elif self.value.value == "length":
                self.interpreter.expect_token("KEYWORD:of")
                self.value = len(ExpressionNode(self.interpreter.next_token()).value)
            elif self.value.value == "split":
                to_split = ExpressionNode(self.interpreter.next_token()).value
                nxt_tkn = self.interpreter.next_token()
                from_ = 0
                till_ = len(to_split)
                if nxt_tkn.type == "KEYWORD":
                    if nxt_tkn.value == "by": self.value = to_split.split(self.interpreter.expect_token("STRING").value)
                    elif nxt_tkn.value in ["from", "till"]:
                        _value = ExpressionNode(self.interpreter.next_token()).value
                        if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "till":
                            self.interpreter.next_token()
                            from_ = _value
                            till_ = ExpressionNode(self.interpreter.next_token()).value
                        else: from_ = _value
                        self.value = to_split[int(from_):int(till_)]
                        
                    else:raise Exception(f"Expected token KEYWORD:by | KEYWORD:from | KEYWORD:to got {nxt_tkn.type}")

                        
                    




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
                func = self.value.interpreter.data["funcs"][self.value.value]
                func_name= self.value.value
                func_interpreter = func[1]
                parased_params = []
                if len(func[0]) > 0: # length of params
                    for param in func[0]: # looping params (func[0] is the param list)
                        e = self.interpreter.get_next_token() # next token, the code afer this checks if it matches the required param
                        if len(param.split(":")) > 1:
                            if e.type==param.split(":")[0].upper():
                                parased_params.append([param.split(":")[1],ExpressionNode(self.interpreter.next_token()).value])
                            else:
                                raise Exception(f"Recieved Token {e.type} instead of {param.split(':')[0]} in function {self.value.value} ") 
                        else:
                            parased_params.append([param,ExpressionNode(self.interpreter.next_token()).value])
                for i in parased_params: func_interpreter.data["vars"][i[0]] = i[1]
                self.value = func_interpreter.compile()

            else: raise Exception(f"Undefined variable {self.value.value}")
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
                list_.append(ExpressionNode(self.interpreter.next_token(),rules=self.rules.append("noLists")).value)
            if len(list_) > 1: self.value = list_
         
class TermNode(Node):
    def __init__(self, factor:Token,rules=[]):
        self.auto_eval = True
        self.interpreter = factor.interpreter
        self.rules = rules
        
        
        tkn1 = FactorNode(factor)
        if self.interpreter.get_next_token().type == "OPERATOR":
            operator = self.interpreter.get_next_token()
            if operator.value in ["*","/","**","^"]:
                operator = self.interpreter.next_token()
                tkn2 = FactorNode(self.interpreter.next_token())
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