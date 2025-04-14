import re
import math

# TODO:
# If Statements
# Asyncio

global rules
rules = {}

class Token:
    def __init__(self, type_, value, interpreter):
        self.type = type_
        self.value = value
        self.interpreter = interpreter

    def __repr__(self):
        return f'({self.type}:{self.value})'


class Node:
    def __init__(self, type_, name, values, auto_eval=False):
        self.type = type_
        self.auto_eval = False
        
        if self.type == "3n":
            self.value1 = values[0]
            self.operator = values[1]
            self.value2 = values[2]

            self.left_node = self.value
            self.operator_node = self.operator
            self.right_node = self.value2
        elif self.type == "2n":
            self.value1 = values[0]
            self.value2 = values[1]

            self.left_node = self.value
            self.right_node = self.operator
        elif self.type == "1n":
            self.value = values[0]
            self.left_node = self.value
        else: raise Exception("Node type not found")
    


class FactorNode(Node):
    def __init__(self, value:Token):
        super().__init__("1n", "FactorNode", [value], auto_eval=True)
        self.interpreter = value.interpreter
        self.value = value
        self.orginal_token = value
        self.auto_eval = True

        self.type = "1n"
        if self.value.type == "SIGNED_NUMBER":
            self.value = float(self.value.value)
        elif self.value.type == "STRING":
            self.value = str(self.value.value)
        elif self.value.type == "BOOL":
            self.value == bool(self.value.value)
        elif self.value.type == "IDENTIFIER":
            if self.value.value in self.value.interpreter.data["vars"]:
                self.value = self.value.interpreter.data["vars"][self.value.value]
            else: raise Exception(f"Undefined variable {self.value.value}")
        elif self.value.type == "LEFT_PAR":
            self.value = ExpressionNode(self.interpreter.next_token()).value
            self.interpreter.next_token()
        else:
            raise Exception("Invalid factor node type")
         
class TermNode(Node):
    def __init__(self, factor:Token):
        self.auto_eval = True
        self.interpreter = factor.interpreter
        
        
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
                elif operator.value == "**":
                    self.value = tkn1.value**tkn2.value
                elif operator.value == "^":
                    self.value = int(tkn1.value)^int(tkn2.value)
            else:
                self.value = tkn1.value
        else:
            self.value = tkn1.value
                
            


class ExpressionNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True

        tkn1 = TermNode(token)
        if token.interpreter.get_next_token().type in ["OPERATOR", "COMPARISION","STRUCTURE"]:
            operator = self.interpreter.next_token()
            tkn2 = TermNode(self.interpreter.next_token())
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
                elif operator.value == "!=":
                    self.value = tkn1.value != tkn2.value
            self.type="3en"
        else:
            self.value = tkn1.value
            self.type="1en"

class ConditionNode(Node):
    def __init__(self,token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True

        self.opposite = False

        if token.type == "LOGIC" and token.value=="not":
            self.opposite = True
            token = self.interpreter.next_token()
        
        tkn1 = ExpressionNode(token)
        if token.interpreter.get_next_token().type == "LOGIC":
            operator = self.interpreter.next_token()
            tkn2 = ExpressionNode(self.interpreter.next_token())
            if operator.value == "and":
                if tkn1.value == True and tkn2.value == True: self.value = True
                else: self.value = False  
            elif operator.value == "or":
                if tkn1.value == True or tkn2.value == True: self.value = True
                else: self.value = False  
           
            self.type="3en"
        else:
            self.value = tkn1.value
            self.type="1en"

        if self.opposite: 
            if self.value == True: self.value = False
            else: self.value = True
        

class IfNode(Node):
    def  __init__(self, token:Token):
        self.interpreter = token.interpreter

        condition = ConditionNode(token).value
        self.interpreter.expect_token("KEYWORD:then")
        self.statement = {
            "main":{"condition":condition,
                 "code": None},
            "else":{
                "code":None
            }

        }
        self.end_found = False
        self.elseif_count = 0


        self.if_interpreter = Interpreter()
        self.if_loop("main")

        self.statement_complete = False

        if condition:
            self.if_interpreter.setup(tokens=self.statement["main"]["code"], data=self.interpreter.data).compile()
            self.statement_complete=True
        else:
            for name in self.statement:
                if self.statement_complete: break
                if type(name) == int:
                    if self.statement[name]["condition"]:
                        self.if_interpreter.setup(tokens=self.statement[name]["code"], data=self.interpreter.data).compile()
                        self.statement_complete = True
        if self.statement_complete != True:
            if self.statement["else"]["code"] != None:
                self.if_interpreter.setup(tokens=self.statement["else"]["code"], data=self.interpreter.data).compile()
                self.statement_complete = True



    def if_loop(self, append_to_name):
        token_blocks = []
        interal_stucture_count = 0

        while self.end_found != True:
            nxt_tkn = self.interpreter.get_next_token()
                                
            if nxt_tkn.type == "STRUCTURE":
                interal_stucture_count +=1
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter=self.if_interpreter
                token_blocks.append(tkn_to_append)
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "end":
                if interal_stucture_count == 0: 
                    self.interpreter.next_token()
                    self.end_found = True
                else: 
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter=self.if_interpreter
                    token_blocks.append(tkn_to_append)
                    interal_stucture_count-=1
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "elseif":
                if interal_stucture_count == 0: # ight then continue with elseif, otherwise the block might be continuing
                    self.interpreter.next_token()
                    condition = ExpressionNode(self.interpreter.next_token()).value
                    self.interpreter.expect_token("KEYWORD:then")

                    self.elseif_count +=1
                    self.statement[self.elseif_count]={"condition":condition,
                    "code": None}
                    self.if_loop(self.elseif_count)

                else:
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter=self.if_interpreter
                    token_blocks.append(tkn_to_append)
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "else":
                self.interpreter.next_token()
                self.if_loop("else")
            else:
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter=self.if_interpreter
                token_blocks.append(tkn_to_append)
        token_blocks.append(Token("ENDSCRIPT","",self.interpreter))
        
        self.statement[append_to_name]["code"] = token_blocks
        

        

        


    


### INTERPRETER


class Interpreter:
    def __init__(self):      
        pass
        
        

    def setup(self, data=None, tokens=None, text=None):
        if data==None:
            self.data = {
                "vars":{

                },
                "funcs":{

                }
            }
        else:
            self.data = data
        if text!=None:self.text=text

        if tokens==None:
            self.tokens = Lexer(text, self).classify_tokens()
        else:
            self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

        return self


        

    def compile(self):

        while self.pos <= len(self.tokens)-1:
            

            if self.current_token.type == "ENDSCRIPT":
                break
            elif self.current_token.type == "NEWLINE":
                self.next_token()
                continue
            if self.current_token.type in ["KEYWORD", "IDENTIFIER","STRUCTURE"]:
                if self.current_token.type == "KEYWORD":
                    if self.current_token.value == "print":
                        print(ExpressionNode(self.next_token()).value)
                    elif self.current_token.value == "set":
                        name = self.expect_token("IDENTIFIER")
                        self.expect_token("KEYWORD:to")
                        value = ExpressionNode(self.next_token())
                        self.data["vars"][name.value] = value.value
                elif self.current_token.type == "STRUCTURE":
                    if self.current_token.value == "if":
                        IfNode(self.next_token())
                else: raise Exception(f"Unexpected Token: {self.current_token}")

                            



            else:
                raise Exception(f"Expected token KEYWORD or VALID_IDENTIFIER, got {self.current_token.type}\n@tusk {self.current_token.value}")
            


            # READER
            #if self.current_token.type == "SET":
                #nxt_tkns = self.expect_tokens("IDENTIFIER;TO;<EXPRESSION>")

            
            # once this shi is done
            if self.get_next_token() == None: break
            else: self.next_token()
            

    def get_var(self, var_name):
        if isinstance(var_name, Token): var_name = var_name.value
        if var_name in self.data["vars"]:
            return self.data["vars"][var_name]
        else:
            raise Exception(f"IDENTIFIER {var_name} is undefined")
    


    def get_next_token(self,nx=0): 
        if self.pos+nx >= len(self.tokens)-1:
            return None
        else: return self.tokens[self.pos+1+nx]
    
    def next_token(self):
        next_tkn = self.get_next_token()
        if next_tkn !=None:
            self.pos+=1
            self.current_token = self.tokens[self.pos]
            return self.current_token
        else:
            raise Exception("Unfinished expression at ENDSCRIPT")
    
    def expect_token(self, token_types):
        token_types = token_types.replace(" ","").split("|")

        next_tkn = self.get_next_token()

        for i in token_types:
            if ":" in i:
                i = i.split(":")[1]
                if next_tkn.value == i:
                    return self.next_token()
            else:
                if next_tkn.type == i:
                    return self.next_token()
        raise Exception(f"Expected token {str(token_types)}, got {next_tkn.type}")
    
    def expect_tokens(self, token_types):
        token_types = token_types.replace(" ","").split(";")
        tokens = []

        for i in token_types:
            if self.get_next_token().type not in i.split("|"):
                raise Exception(f"Expected token {str(token_types)}, got {self.current_token.type}")
            else: 
                tokens.append(self.get_next_token())
                self.next_token()
        
        return tokens
    

        


class Lexer:
    def __init__(self,text, interpreter):
        self.text = text

        self.pos = 0
        self.current_token = None

        self.tokens = []

        self.interpreter = interpreter
      

    
    def classify_tokens(self):
        stuff = self.text.split()

        text = self.text
        reader_pos = 0
        token = ""

        in_string = False
        in_comment = False
        start_quote_type = None     

        for j in text: 
            

            if in_string:
                if j == start_quote_type:
                    in_string = False
                    self.tokens.append(Token("STRING", token, self.interpreter))
                    token = ""
                else:
                    token += j
            elif in_comment:
                if j == "\n":
                    in_comment = False
                    token = ""
                else: pass
            else:
                if j in "(){}[]":
                    token_type = {
                        "(": "LEFT_PAR",
                        ")": "RIGHT_PAR",
                        "{": "LEFT_CURLY",
                        "}": "RIGHT_CURLY",
                        "[": "LEFT_SQUARE",
                        "]": "RIGHT_SQUARE"
                    }[j]
                    self.tokens.append(Token(token_type, token, self.interpreter))
                    token = ""
                elif j == "#":
                    in_comment = True
                    token = ""
                elif j in ["'", '"']:
                    in_string = True
                    start_quote_type = j
                    token = ""
                elif j in " \t\n" or reader_pos == len(text)-1:
                    if reader_pos == len(text)-1: token += j
                    if j in "\n":
                        self.tokens.append(Token("NEWLINE", token, self.interpreter))
                        token = ""
                    if token != "":
                        if token.isnumeric():
                            self.tokens.append(Token("SIGNED_NUMBER", token, self.interpreter))
                            token = ""
                        elif token in ["true","false"]:
                            self.tokens.append(Token("BOOL", token, self.interpreter))
                            token = ""
                        elif token in ["and","or","not"]:
                            self.tokens.append(Token("LOGIC", token, self.interpreter))
                            token = ""
                        elif token in ["<", ">", "<=", ">=", "==", "!="]:
                            self.tokens.append(Token("COMPARISION", token, self.interpreter))
                            token = ""
                        elif token in ["set", "to", "print", "then", "elseif", "else", "end"]:
                            self.tokens.append(Token("KEYWORD", token, self.interpreter))
                            token=""
                        elif token in ["if","while","for","create"]:
                            self.tokens.append(Token("STRUCTURE", token, self.interpreter))
                            token=""
                        elif token in ["+", "-", "*", "/","**", "%"]:
                            self.tokens.append(Token("OPERATOR", token, self.interpreter))
                            token=""
                        else:
                            self.tokens.append(Token("IDENTIFIER", token, self.interpreter))
                            token = ""
                        
                        
                    

                    
                    
                    """
                    if j in "   ":
                        self.tokens.append(Token("TAB", token, self.interpreter))
                        token = ""                   
                    elif token == " ":
                        self.tokens.append(Token("WHITESPACE", token, self.interpreter))
                        token = ""
                    """
                else:
                    token += j

            reader_pos+= 1


                    
            '''
            elif token in " \t\n":
                self.tokens.append(Token("WHITESPACE", token))
            '''

        self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))

        ##  All this tab shi was done by chatgpt, it works so don't touch it
        """
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].type == "TAB":
                start = i
                count = 1
                while i + count < len(self.tokens) and self.tokens[i + count].type == "TAB":
                    count += 1

                tab_token = self.tokens[i]
                tab_groups = count // 4

                del self.tokens[start:start + count]

                for _ in range(tab_groups):
                    self.tokens.insert(start, Token("TAB", tab_token.value, self.interpreter))

                i = start + tab_groups
            else:
                i += 1
        i = 0
        while i < len(self.tokens) - 1:
            if self.tokens[i].type == "TAB" and self.tokens[i + 1].type == "NEWLINE":
                del self.tokens[i]
            else:
                i += 1


        # ight you can touch it now
        """

        return self.tokens
        
            
            

with open("test.tusk", "r") as f:
    code = f.read()

TuskTestInterpreter = Interpreter()
TuskTestInterpreter.setup(text=code)
TuskTestInterpreter.compile()
