import re
import math
import asyncio
import discord
import json

from logger import *
from tusk.lexer import *

from tusk.nodes.expressions import FactorNode, TermNode, ExpressionNode
from tusk.nodes.statement import StatementNode
from tusk.nodes.base.function import FunctionNode
from tusk.nodes.base.return_node import ReturnNode

### INTERPRETER

class Interpreter:
    def __init__(self):      
        self.return_value = True

    def setup(self, data=None, tokens=None, text=None, bot=None, file=None):
        if data==None:
            self.data = {
                "vars":{},
                "funcs":{},
                "local":{},
                "async_tasks":[],
                "events":{
                    "message":[],
                    "reaction":[],
                    "voice":[],
                    "join":[],
                    "leave":[],
                    "typing":[]
                }
            }
        else:
            self.data = data
        if text!=None:self.text=text
        if file!=None:
            with open(file, "r") as f:
                self.text = f.read()
            self.file=file
        else: self.file = "<stdin>"

        if tokens==None:
            self.tokens = Lexer(self.text, self).classify_tokens()
        else:
            self.tokens = tokens
            self.tokens = self.change_token_parent(self)
        if bot == None:
            self.error("BotNotFound", "The bot specified does not exist", notes=["This error is caused by setup, it is not script-side error"])
        self.bot = bot
        self.pos = 0
        self.current_token = self.tokens[self.pos]

        with open('config.json', 'r') as f:
            self.config = json.load(f)
        self.debug = self.config["debug"]
        self.debug_msg(self.tokens, self.data)
        return self

    async def compile(self):
        while self.pos <= len(self.tokens)-1:
            #self.debug_msg(self.current_token, "<- stmt start")
            if self.current_token.type == "ENDSCRIPT":
                print("? ENDSCRIPT")
                return self.return_value
            elif self.current_token.type == "NEWLINE":
                self.next_token()
                continue
            elif self.current_token.type == "BREAKSTRUCTURE" and self.current_token.value == "return":
                await ReturnNode(self.current_token).create()
                break
            else:
                
                if self.current_token.type == "ENDSCRIPT": 
                    debug_print("FAILCHECK ENDSCRIPT")
                    return self.return_value
                try:
                    await StatementNode(self.current_token).create()
                except Exception as e:
                    self.error("UnknownError", str(e))
                    raise e
            self.debug_msg(self.current_token, "<- stmt end")
            if self.get_next_token() == None: 
                debug_print("MISS ENDSCRIPT")
                break
            else: 
                e = self.next_token()
                if e.type == "ENDSCRIPT": 
                    debug_print("DEFAULT ENDSCRIPT")
                    return self.return_value


    def change_token_parent(self, interpreter):
        tokens = []
        for token in self.tokens:
            token.interpreter = interpreter
            tokens.append(token)
        return tokens
    
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
            npos += 1
            if npos >= self.pos-2 and npos <= self.pos+4:
                # Format token value
                if i.type == "STRING":
                    token_str = f' "{i.value}"'
                    width = len(i.value) + 3
                else:
                    token_str = f" {i.value}"
                    width = len(i.value) + 1
                
                recreated_code += token_str
                
                # Add arrows
                if npos == self.pos+1:
                    arrows += "^" * width
                    target = i
                else:
                    arrows += " " * width
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
        self.debug_msg(next_tkn, "<- to be expected token")
        for i in token_types:
            if ":" in i:
                i = i.split(":")[1]
                if next_tkn.value == i:
                    return self.next_token()
            else:
                if next_tkn.type == i:
                    return self.next_token()
        if "IDENTIFIER" in token_types:
            self.error("UnexpectedToken",f"Expected token {str(token_types)}, got {next_tkn.type}", notes=["Possible Fix: You might have entered a keyword as a variable name, try renaming it"])
        else:
            self.error("UnexpectedToken",f"Expected token {str(token_types)}, got {next_tkn.type}")
    
    def expect_tokens(self, token_types):
        token_types = token_types.replace(" ","").split(";")
        tokens = []

        for i in token_types:
            if self.get_next_token().type not in i.split("|"):
                raise Exception(f"Expected token {str(token_types)}, got {self.current_token}")
            else: 
                tokens.append(self.get_next_token())
                self.next_token()
        
        return tokens
    
    def error(self, error_name, error_desc, notes=[]):
        print("================ ERROR ================")
        print(f"{error_name}: {error_desc}")
        print("============== POSITION ===============")
        print(self.arrows_at_pos())
        print("================ NOTES ================")
        for i in notes:
            print(i)
        print("=======================================")
        #exit()

    def debug_msg(self, *args,color="blue"):
        if self.debug: cprint(*args,color=color,engine="debug")
    
    def print_(self,*args,color="normal",engine="tusk"):
        cprint(*args,color=color,engine=f"{engine}@{self.file}")
        



        
            
            


