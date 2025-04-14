import re


# TODO:
# - Add support for multiline strings
# FIX: Use a regular reader instead of splitting it into lists in Lexer
# OPTIONAL: Add support for whitepaces

global rules
rules = {}

class Token:
    def __init__(self, type_, value, lexer):
        self.type = type_
        self.value = value
        self.lexer = lexer

    def __repr__(self):
        return f'({self.type}:{self.value})'

'''
class Rule:
    def __init__(self,name, rule):
        self.name = name
        self.rule = rule
        
        rules[name] = rule

    def do_rule(self, lexer):  # lexer is an interpreter
        """
        Parses tokens based on the rule logic and returns a list of matched tokens.

        Examples:
        
        factor: IDENTIFIER | SIGNED_NUMBER | STRING 
        term: (<factor>; OPERATOR:/ | OPERATOR:* ; <factor>) | <factor>
        expression: (<term>; OPERATOR:+ | OPERATOR:- ; <term>) | <term>

        condition: (<expression> COMPARISION <expression>)

        Explanation:

        rule: RULE LOGIC
        Your rule logic works like this:

        - Every word/token/sub-rule will be separated by semicolon, this will be the order to expect it. 
            By default, you don't need to group it in () but if you have multiple methods for that rule like in the example where <term> has another method called <factor>,
            here you need to group everything that has a semicolon inside the () and then separate it with | 
            Example: term: (<factor>; OPERATOR:/ | OPERATOR:* ; <factor>) | <factor>
        - Tokens are capitalized & if you want a specific token add a colon and type the token value; example: OPERATOR:+ or OPERATOR:* 
        - You can also use sub-rules which are stored in the global rules dict. Sub-rules exist so you don't have to repeat a rule again if it's in the rule you're making.
            Sub-rules are also separated by semicolons and can be used in the same way as tokens. Example: <term>; <factor> | <factor>
            To use one just <RULE_NAME>
        """
        
        tokens = []

        broken_str = self.rule

        # Get all sub-rules
        while "<" in broken_str:
            
            start = broken_str.index("<")
            if broken_str[start-1] != ":": # To check if the previous char was a : cuz we don't want to replace it if it was a token
                rule_name = ""
                for i in broken_str[start:]:
                    rule_name+=i
                    if i == ">": 
                        break

                rule_value = rules[rule_name.replace("<","").replace(">","")] 

                broken_str = broken_str.replace(rule_name, rule_value)

                print(broken_str)

        

            


        return tokens

    def __repr__(self):
        return f'<{self.name}>: {self.rule}'
'''  

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
    
    def __repr__(self):
        if self.type == "3n":
            if self.auto_eval:
                return f"({self.left_node} {self.operator_node} {self.right_node})"
            return f"(<{self.left_node} {self.operator_node} {self.right_node}>)"
        elif self.type == "2n":
            if self.auto_eval:
                return f"({self.left_node} {self.right_node})"
            return f"(<{self.left_node} {self.right_node}>)"
        elif self.type == "1n":
            if self.auto_eval:
                return f"({self.left_node})"
            return f"(<{self.left_node}>)"


class FactorNode(Node):
    def __init__(self, value:Token):
        super().__init__("1n", "FactorNode", [value], auto_eval=True)
        self.value = value
        self.auto_eval = True

        self.type = "1n"

        if self.value.type == "SIGNED_NUMBER":
            self.value = int(self.value.value)
        elif self.value.type == "STRING":
            self.value = str(self.value.value)
        else:
            raise Exception("Invalid factor node type")
 
class TermNode(Node):
    def __init__(self, left_node:FactorNode, operator_node:Token, right_node:FactorNode):
        super().__init__("3n", "TermNode", [left_node, operator_node, right_node], auto_eval=True)
        self.left_node = left_node
        self.operator_node = operator_node
        self.right_node = right_node
        self.auto_eval = True

        # Calculating It
        self.type = "1n"

        # Simplifiying It


        

        if self.left_node.type=="SIGNED_NUMBER" and self.right_node.type=="SIGNED_NUMBER":
            self.value = self.operator()
        elif self.left_node.type=="STRING" and self.right_node.type=="STRING" and self.operator_node.value=="+":
            self.value = self.operator()
        else:
            raise Exception(f"Invalid operation ({self.operator_node}) between {self.left_node.type} and {self.right_node.type}")
        
        del self.left_node
        del self.right_node
            

    def operator(self):
        if self.operator_node.type == "OPERATOR":
            if self.operator_node.value == "+":
                return self.left_node.value + self.right_node.value
            elif self.operator_node.value == "-":
                return int(self.left_node.value) - int(self.right_node.value)
            elif self.operator_node.value == "*":
                return int(self.left_node.value) * int(self.right_node.value)
            elif self.operator_node.value == "/":
                return int(self.left_node.value) / int(self.right_node.value)
            elif self.operator_node.value == "^":
                return int(self.left_node.value) ** int(self.right_node.value)
            elif self.operator_node.value == "%":
                return int(self.left_node.value) % int(self.right_node.value)
            else: raise Exception("Operator not found")
        else: raise Exception("Operator not found")

        


    


### INTERPRETER

class Interpreter:
    def __init__(self,text):
        self.text = text

        self.pos = 0
        self.current_token = None

        self.tokens = []
        self.vars = {}

    def compile(self):
        self.tokens = self.classify_tokens()

        self.pos = 0 # reset the reader cuz we used it in the lexer
        self.current_token = self.tokens[self.pos] 

        print("================= DEBUG ==================")
        print(self.tokens)
        print("================= OUTPUT =================")
        while self.pos <= len(self.tokens)-1:
            
            print(self.current_token)

            if self.current_token.type in ["KEYWORD", "IDENTIFIER"]:
                if self.current_token.type == "KEYWORD":
                    if self.current_token.value == "print":
                        print(self.expect_token("STRING|IDENTIFIER|SIGNED_NUMBER").value)
            else:
                raise Exception(f"Expected token KEYWORD or VALID_IDENTIFIER, got {self.current_token.type}\n@tusk {self.current_token.value}")
            


            # READER
            #if self.current_token.type == "SET":
                #nxt_tkns = self.expect_tokens("IDENTIFIER;TO;<EXPRESSION>")

            
            # once this shi is done
            if self.get_next_token() == None: break
            else: self.next_token()
            


    
    def get_next_token(self): 
        if self.pos >= len(self.tokens)-1: 
            return None
        else: return self.tokens[self.pos+1]
    
    def next_token(self):
        next_tkn = self.get_next_token()
        if next_tkn !=None:
            self.pos+=1
            self.current_token = self.tokens[self.pos]
            return self.current_token
    
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
    
        '''
        if self.get_next_token().type not in token_types:
            raise Exception(f"Expected token {str(token_types)}, got {self.current_token.type}")
        else: return self.next_token()
        '''
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
    
    def expect_segments(self, statement):
        """
        Parses tokens based on the rule logic and returns a list of matched tokens.

        Examples:
        
        factor: IDENTIFIER | SIGNED_NUMBER | STRING 
        term: (<factor>; OPERATOR:/ | OPERATOR:* ; <factor>) | <factor>
        expression: (<term>; OPERATOR:+ | OPERATOR:- ; <term>) | <term>

        condition: (<expression> COMPARISION <expression>)

        Explanation:

        rule: RULE LOGIC
        Your rule logic works like this:

        - Every word/token/sub-rule will be separated by semicolon, this will be the order to expect it. 
            By default, you don't need to group it in () but if you have multiple methods for that rule like in the example where <term> has another method called <factor>,
            here you need to group everything that has a semicolon inside the () and then separate it with | 
            Example: term: (<factor>; OPERATOR:/ | OPERATOR:* ; <factor>) | <factor>
        - Tokens are capitalized & if you want a specific token add a colon and type the token value; example: OPERATOR:+ or OPERATOR:* 
        - You can also use sub-rules which are stored in the global rules dict. Sub-rules exist so you don't have to repeat a rule again if it's in the rule you're making.
            Sub-rules are also separated by semicolons and can be used in the same way as tokens. Example: <term>; <factor> | <factor>
            To use one just <RULE_NAME>
        """

        e = re.match(
            r"(?P<rule_name>[a-zA-Z_][a-zA-Z0-9_]*):\s*(?P<rule_logic>.+)",
            statement
        )
        print(e)


    

    
    def classify_tokens(self):

        print("================= LEXER ==================")
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
                    self.tokens.append(Token("STRING", token, self))
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
                    self.tokens.append(Token(token_type, token, self))
                    token = ""
                elif j == "#":
                    in_comment = True
                    token = ""
                elif j in ["'", '"']:
                    in_string = True
                    start_quote_type = j
                    token = ""
                elif j in " \t\n":
                    if token != "":
                        if token.isnumeric():
                            self.tokens.append(Token("SIGNED_NUMBER", token, self))
                            token = ""
                        elif token in ["<", ">", "<=", ">=", "==", "!="]:
                            self.tokens.append(Token("COMPARISION", token, self))
                            token = ""
                        elif token in ["set", "to", "print", "if", "then", "elseif", "else", "end"]:
                            self.tokens.append(Token("KEYWORD", token, self))
                        elif token in ["+", "-", "*", "/","^", "%"]:
                            self.tokens.append(Token("OPERATOR", token, self))
                        else:
                            self.tokens.append(Token("IDENTIFIER", token, self))
                            token = ""
                    # self.tokens.append(Token("WHITESPACE", j, self)) Skipping whitespaces for now
                else:
                    token += j


                    


            """
            if token.startswith("("):
                token = token[1:]
                self.tokens.append(Token("LEFT_PAR", "(", self))
            elif token.endswith(")"):
                token = token[:-1]
                self.tokens.append(Token("RIGHT_PAR", ")", self))
            elif token.startswith('"') | token.startswith("'"): # Strings
                start_quote_type = token[0]
                partial_string = ""

                reader = iter(self.text[self.text.index(token):])
                current_char = next(reader, None)
                formed_token=""
                while current_char != None:
                    partial_string += current_char
                    current_char = next(reader, None)
                    if current_char == start_quote_type:
                        break
                    elif current_char == None:
                        raise Exception("Unclosed string")
                partial_string = partial_string[1:]

                e = (start_quote_type+partial_string+start_quote_type)
                for i in e.split():
                    stuff.pop(stuff.index(i))


                self.tokens.append(Token("STRING", partial_string, self))
            elif token.isnumeric():
                self.tokens.append(Token("SIGNED_NUMBER", token, self))
            elif token in ["<", ">", "<=", ">=", "==", "!="]:
                self.tokens.append(Token("COMPARISION", token, self))
            elif token in ["set", "to", "print", "if", "then", "elseif", "else", "end"]:
                self.tokens.append(Token("KEYWORD", token, self))
            elif token in ["+", "-", "*", "/","^", "%", "**"]:
                self.tokens.append(Token("OPERATOR", token, self))            
            else:
                self.tokens.append(Token("IDENTIFIER", token, self))

            """

            '''
            elif token in " \t\n":
                self.tokens.append(Token("WHITESPACE", token))
            '''

        
        return self.tokens
        
            
            


                





        
with open("test.tusk", "r") as f:
    code = f.read()

TuskTestInterpreter = Interpreter(code)
TuskTestInterpreter.compile()
