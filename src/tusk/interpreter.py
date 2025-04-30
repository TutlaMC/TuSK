import re
import math
import asyncio

from tusk.lexer import *

from tusk.nodes.expressions import FactorNode, TermNode, ExpressionNode
from tusk.nodes.statement import StatementNode
from tusk.nodes.base.function import FunctionNode
from tusk.nodes.base.return_node import ReturnNode

### INTERPRETER



class Interpreter:
    def __init__(self):      
        self.return_value =  True
        
        

    def setup(self, data=None, tokens=None, text=None):
        if data==None:
            self.data = {
                "vars":{

                },
                "funcs":{

                },
                "local":{

                },
                "async_tasks":[]
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
            elif self.current_token.type == "BREAKSTRUCTURE" and self.current_token.value == "return":
                ReturnNode(self.current_token)
                break
            else:
                try:
                    StatementNode(self.current_token)
                except Exception as e:
                    print(e)
                    print(self.arrows_at_pos())
                    raise e

            # READER
            #if self.current_token.type == "SET":
                #nxt_tkns = self.expect_tokens("IDENTIFIER;TO;<EXPRESSION>")

            
            # once this shi is done
            if self.get_next_token() == None: break
            else: self.next_token()



        return self.return_value
            

    def get_var(self, var_name):
        if isinstance(var_name, Token): var_name = var_name.value
        if var_name in self.data["vars"]:
            return self.data["vars"][var_name]
        else:
            raise Exception(f"IDENTIFIER {var_name} is undefined")
    

    def arrows_at_pos(self):
        recreated_code = ""
        arrows=""
        npos = 0
        target=""
        for i in self.tokens:
            npos+=1
            if npos < self.pos and npos > self.pos-4:
                if i.type == "STRING":
                    recreated_code+=' "'+i.value+'"'
                    tar = len(i.value)+3
                else: 
                    recreated_code+=" "+i.value
                    tar = len(i.value)+1
                arrows += "*" * (tar-1)
            elif npos > self.pos and npos < self.pos+4:
                if i.type == "STRING":
                    recreated_code+=' "'+i.value+'"'
                    tar = len(i.value)+3
                else: 
                    recreated_code+=" "+i.value
                    tar = len(i.value)+1
                arrows += "*" * (tar-1)
            elif npos == self.pos:
                if i.type == "STRING":
                    recreated_code+=' "'+i.value+'"'
                    tar = len(i.value)+3
                else: 
                    recreated_code+=" "+i.value
                    tar = len(i.value)+1
                arrows += "^" * (tar-1)
                target=i
        recreated_code+=f"<---- {str(target)}"
                
        return f"{recreated_code}\n{arrows}"
            


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
    

    

        



        
            
            


