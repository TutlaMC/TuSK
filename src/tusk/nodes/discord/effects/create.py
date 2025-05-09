import discord

from tusk.node import Node
from tusk.token import Token

from tusk.discord_classes import *

class CreateNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self): # TODO: Add Permission Support, emoji support
        from tusk.nodes.expressions import ExpressionNode
        to_create = self.interpreter.expect_token("KEYWORD:channel|KEYWORD:role|KEYWORD:emoji")
        if to_create == "channel":
            self.interpreter.expect_token("KEYWORD:named")
            name = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.interpreter.expect_token("LOGIC:in")
            guild = (await ExpressionNode(self.interpreter.next_token()).create()).value
            guild = to_discord_object(self.interpreter.bot,guild,"guild")
            if guild is None:
                raise Exception(f"Guild {guild} not found")
            c = await guild.create_text_channel(name)
            self.value = ChannelClass(c)
        elif to_create == "role":
            self.interpreter.expect_token("KEYWORD:named")
            name = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.interpreter.expect_token("LOGIC:in")
            guild = (await ExpressionNode(self.interpreter.next_token()).create()).value
            guild:discord.Guild = to_discord_object(self.interpreter.bot,guild,"guild")

            color = None
            if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "with":
                while self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value in ["color"]:
                    typ = self.interpreter.next_token()
                    if typ == "color":
                        color = self.interpreter.next_token()
                        if color.type == "COLOR":
                            color = color.value
                        else:
                            raise Exception(f"Color {color} is not a color")
                    
                    if self.interpreter.get_next_token().value != "and":
                        break
            if guild is None:
                raise Exception(f"Guild {guild} not found")
            if color is None:
                color = 0x000000
            e = await guild.create_role(name,color=color)
            self.value = RoleClass(e)
        elif to_create == "emoji":
            # coming soon
            pass

        return self