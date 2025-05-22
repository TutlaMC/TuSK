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

from tusk.discord_classes import *

### INTERPRETER

class Interpreter:
    def __init__(self):      
        self.return_value = True

    def setup(self, data=None, tokens=None, text=None, bot=None, file=None, is_cmd=False):
        if data==None:
            self.data = {
                "vars":{},
                "funcs":{},
                "local":{},
                "async_tasks":[],
                "events":get_exec_names()
            }
        else:
            self.data = data
        if text!=None:self.text=text
        if file!=None:
            with open(file, "r") as f:
                self.text = f.read()
            self.file=file
            if is_cmd:
                self.text = "\n".join(self.text.split("\n")[1:])
        else: self.file = "<stdin>"

        if tokens==None:
            self.tokens = Lexer(self.text, self).classify_tokens()
        else:
            self.tokens = tokens 
            self.tokens = self.change_token_parent(self) 
        if bot == None:
            self.error("BotNotFound", "The bot specified does not exist", notes=["This error is caused by setup, it is not script-side error"])
        self.bot:discord.Client|discord.Bot = bot
        if hasattr(self.bot, "user"):
            self.data["vars"]["me"] = UserClass(self.bot.user)
            self.data["vars"]["myself"] = self.data["vars"]["me"]
            self.data["vars"]["I"] = self.data["vars"]["me"]
            self.data["vars"]["my"] = self.data["vars"]["me"]

            if len(self.bot.guilds) > 0:
                self.data["vars"]["my_guild"] = GuildClass(self.bot.guilds[0])
                self.data["vars"]["my_server"] = self.data["vars"]["my_guild"]

                for i in self.bot.guilds[0].channels:
                    if "general" in i.name.lower() and type(i) == discord.TextChannel:
                        self.data["vars"]["my_channel"] = ChannelClass(i)
                        
            

        self.pos = 0
        self.current_token = self.tokens[self.pos]

        with open('config.json', 'r') as f:
            self.config = json.load(f)
        self.debug = self.config["debug"]
        self.debug_msg(self.tokens)
        return self

    async def compile(self):
        self.end_found = False
        self.caught_error = False
        while self.pos <= len(self.tokens)-1:
            #self.debug_msg(self.current_token, "<- stmt start")
            if self.end_found:
                self.debug_msg("RETURN ENDSCRIPT")
                return self.return_value
            if self.current_token.type == "ENDSCRIPT":
                self.debug_msg("DEFAULT ENDSCRIPT", "<- stmt end")
                return self.return_value
            elif self.current_token.type == "NEWLINE":
                self.next_token()
                continue
            elif self.current_token.type == "BREAKSTRUCTURE" and self.current_token.value == "return":
                await ReturnNode(self.current_token).create()
                break
            else:
                
                if self.current_token.type == "ENDSCRIPT": 
                    self.debug_msg("FAILCHECK ENDSCRIPT", "<- stmt end")
                    return self.return_value
                try:
                    await StatementNode(self.current_token).create()
                except Exception as e:
                    self.error("UnknownError", str(e))
                    raise e
            self.debug_msg(self.current_token, "<- stmt end")
            if self.get_next_token() == None: 
                self.debug_msg("MISS ENDSCRIPT", "<- stmt end")
                break
            else: 
                e = self.next_token()
                if e.type == "ENDSCRIPT": 
                    self.debug_msg("DEFAULT ENDSCRIPT", "<- stmt end")
                    return self.return_value


    def change_token_parent(self, interpreter) -> list[Token]:
        tokens = []
        for token in self.tokens:
            token.interpreter = interpreter
            tokens.append(token)
        return tokens
    
    def get_var(self, var_name) -> any:
        if isinstance(var_name, Token): var_name = var_name.value
        if var_name in self.data["vars"]:
            return self.data["vars"][var_name]
        else:
            raise Exception(f"IDENTIFIER {var_name} is undefined")
    

    def arrows_at_pos(self) -> str:
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
            


    def get_next_token(self,nx=0) -> Token|None: 
        if self.pos+nx >= len(self.tokens)-1:
            return None
        else: return self.tokens[self.pos+1+nx]
    
    def is_token(self,token_type) -> bool:
        token_type = token_type.split(":")
        if self.get_next_token().value == token_type[1] and self.get_next_token().type == token_type[0]:
            return True
        else:
            return False

    def next_token(self) -> Token:
        next_tkn = self.get_next_token()
        if next_tkn !=None:
            self.pos+=1
            self.current_token = self.tokens[self.pos]
            return self.current_token
        else:
            self.error("UnfinishedExpression", "Unfinished expression at ENDSCRIPT")
    
    def expect_token(self, token_types, notes:list[str]=[]) -> Token:
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
            self.error("UnexpectedToken",f"Expected token {str(token_types)}, got {next_tkn}", notes=["Possible Fix: You might have entered a keyword as a variable name, try renaming it"])
        else:
            self.error("UnexpectedToken",f"Expected token {str(token_types)}, got {next_tkn}",notes=notes)
    
    def expect_tokens(self, token_types) -> list[Token]:
        token_types = token_types.replace(" ","").split(";")
        tokens = []

        for i in token_types:
            if self.get_next_token().type not in i.split("|"):
                raise Exception(f"Expected token {str(token_types)}, got {self.current_token}")
            else: 
                tokens.append(self.get_next_token())
                self.next_token()
        
        return tokens
    
    def error(self, error_name:str, error_desc:str, notes:list[str]=[]):
        if not self.caught_error: # to prevent error spam
            self.caught_error = True
            print("\n================ ERROR ================")
            print(f"{error_name}: {error_desc}")
            print("============== POSITION ===============")
            print(self.arrows_at_pos())
            print("================ NOTES ================")
            for i in notes:
                print(i)
            print("=======================================\n")
            self.end_found = True
            #exit()
        self.caught_error = True

    def debug_msg(self, *args,color="blue"):
        if self.debug: cprint(*args,color=color,engine="debug")
    
    def print_(self,*args,color="normal",engine="tusk"):
        cprint(*args,color=color,engine=f"{engine}@{self.file}")
        



        
            
            


