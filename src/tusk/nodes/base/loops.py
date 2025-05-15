from tusk.node import Node
from tusk.token import Token
from tusk.nodes.condition import *
from tusk.discord_classes import to_discord_object, to_tusk_object
import discord 
class WhileNode(Node):
    def __init__(self, token: Token):
        from tusk.interpreter import Interpreter
        from tusk.nodes.statement import StatementNode
        self.token = token
        self.interpreter = token.interpreter
        self.cpos = self.interpreter.pos # position of condition start
        self.ecpos = self.cpos # position at ENDSTRUCTURE

    async def create(self):
        from tusk.nodes.statement import StatementNode
        await self.check()
        
        fned = False
        internal_structure_count = 0
        while fned != True:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                if internal_structure_count == 0:
                    self.ecpos = self.interpreter.pos
                    fned = True
                else:
                    internal_structure_count -= 1
            elif nxt_tkn.type == "STRUCTURE":
                internal_structure_count += 1
            else: 
                self.interpreter.next_token()
        self.interpreter.pos = self.cpos
        await self.check() # this is just to skip the condition   
        
        internal_structure_count = 0
        while self.end_done:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                if internal_structure_count == 0:
                    await self.check()
                else:
                    internal_structure_count -= 1
            elif nxt_tkn.type == "STRUCTURE":
                internal_structure_count += 1
            else: 
                await StatementNode(nxt_tkn).create()

             # recheck the condition
        self.interpreter.pos = self.ecpos
        return self

    async def check(self):
        self.interpreter.pos = self.cpos
        condition = await ConditionNode(self.token).create()
        self.interpreter.expect_token("KEYWORD:do")
        self.end_done = condition.value
        return self
    
    """
    async def create(self):
        from tusk.nodes.statement import StatementNode
        condition = await ConditionNode(self.token).create()
        self.interpreter.expect_token("KEYWORD:do")

        self.end_done = condition.value
        
        fned = False
        internal_structure_count = 0
        while fned != True:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                if internal_structure_count == 0:
                    self.ecpos = self.interpreter.pos
                    fned = True
                else:
                    internal_structure_count -= 1
            elif nxt_tkn.type == "STRUCTURE":
                internal_structure_count += 1
            else: 
                self.interpreter.next_token()
        self.interpreter.pos = self.cpos
        await ConditionNode(self.token).create()       
        
        while self.end_done:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                await self.check()
            else: 
                await StatementNode(nxt_tkn).create()

             # recheck the condition
        self.interpreter.pos = self.ecpos
        return self

    async def check(self):
        self.interpreter.pos = self.cpos
        condition = await ConditionNode(self.token).create()
        self.interpreter.expect_token("KEYWORD:do")
        self.end_done = condition.value
        return self
    """
            
class LoopNode(Node):
    def __init__(self, token: Token):        
        self.token = token
        self.interpreter = token.interpreter
        

        self.as_ = None
        self.times = 0

    async def create(self):
        from tusk.nodes.expressions import FactorNode, ExpressionNode
        if self.token.type=="NUMBER":
            self.times = range(int((await FactorNode(self.token).create()).value))
            self.interpreter.expect_token("KEYWORD:times")
            e = await self.set_as(token=self.interpreter.get_next_token())
            await self.loop()
        elif self.token.type=="KEYWORD" and self.token.value == "all":
            loop_target_type = self.interpreter.expect_token("KEYWORD:items|KEYWORD:characters|KEYWORD:channels|KEYWORD:servers|KEYWORD:members|KEYWORD:users|KEYWORD:messages|KEYWORD:categories|KEYWORD:emojis").value
            self.interpreter.expect_token("LOGIC:in")
            if loop_target_type == "characters":
                self.times = str((await ExpressionNode(self.interpreter.next_token()).create()).value)
                e = await self.set_as(token=self.interpreter.get_next_token())
                await self.loop()
            elif loop_target_type == "items":
                self.times = (await ExpressionNode(self.interpreter.next_token()).create()).value
                print(self.times,"times")
                e = await self.set_as(token=self.interpreter.get_next_token())
                await self.loop()
            elif loop_target_type == "channels":
                self.times = (await ExpressionNode(self.interpreter.next_token()).create()).value
                self.times:discord.Guild = await to_discord_object(self.interpreter.bot, self.times, "guild")
                channels = await self.times.fetch_channels()
                self.times = await to_tusk_object(self.interpreter.bot, channels, "channel", references=[self.times])
                e = await self.set_as(token=self.interpreter.get_next_token(),fallback="loop_channel")
                await self.loop()
            elif loop_target_type == "servers":
                self.times = (await ExpressionNode(self.interpreter.next_token()).create()).value
                servers = await self.interpreter.bot.fetch_guilds()
                self.times = await to_tusk_object(self.interpreter.bot, servers, "server", references=[self.times])
                e = await self.set_as(token=self.interpreter.get_next_token(),fallback="loop_server")
                await self.loop()
            elif loop_target_type in ["members","users"]:
                self.times = (await ExpressionNode(self.interpreter.next_token()).create()).value
                self.times:discord.Guild = await to_discord_object(self.interpreter.bot, self.times, "guild")
                members = await self.times.fetch_members()
                self.times = await to_tusk_object(self.interpreter.bot, members, "user", references=[self.times])
                e = await self.set_as(token=self.interpreter.get_next_token(),fallback="loop_member")
                await self.loop()
            elif loop_target_type == "categories":
                self.times = (await ExpressionNode(self.interpreter.next_token()).create()).value
                self.times:discord.Guild = await to_discord_object(self.interpreter.bot, self.times, "guild")
                categories = await self.times.categories
                self.times = await to_tusk_object(self.interpreter.bot, categories, "category", references=[self.times])
                e = await self.set_as(token=self.interpreter.get_next_token(),fallback="loop_category")
                await self.loop()
            elif loop_target_type == "emojis":
                self.times = (await ExpressionNode(self.interpreter.next_token()).create()).value
                self.times:discord.Guild = await to_discord_object(self.interpreter.bot, self.times, "guild")
                emojis = await self.times.fetch_emojis()
                self.times = await to_tusk_object(self.interpreter.bot, emojis, "emoji", references=[self.times])
                e = await self.set_as(token=self.interpreter.get_next_token(),fallback="loop_emoji")
                await self.loop()
            else:
                raise Exception(f"loop expected token KEYWORD | NUMBER got {self.token.type}")
        return self

    async def set_as(self, token:Token=None,value=None,fallback="loop_item"):
        if value != None:
            self.interpreter.data["vars"][self.as_] = value
        else:
            if token.type == "KEYWORD" and token.value == "as":
                self.interpreter.next_token()
                var = self.interpreter.next_token()
                if var.type == "IDENTIFIER":
                    self.as_ = var.value
                    self.interpreter.data["vars"][str(var.value)] = None
            else:
                self.as_ = fallback
                self.interpreter.data["vars"][self.as_] = None
        return self

    async def loop(self):
        from tusk.nodes.statement import StatementNode
        from tusk.variable import Variable
        from tusk.nodes.base.name import setter
        pos = self.interpreter.pos
        run = True
        for i in self.times: 
            setter(self.as_,i,self.interpreter)
            end_block = False
            self.interpreter.pos = pos
            while end_block == False:
                nxt_tkn = self.interpreter.next_token()
                if nxt_tkn.type == "ENDSTRUCTURE":
                    end_block =True
                    break
                elif nxt_tkn.type == "BREAKSTRUCTURE" and nxt_tkn.value == "break":
                    run = False
                    break
                else:
                    if run == True:
                        await StatementNode(nxt_tkn).create()