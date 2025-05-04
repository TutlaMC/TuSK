from tusk.node import Node
from tusk.token import Token

from tusk.discord_classes import MessageClass


import asyncio
import discord

class SendNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        message = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:to")
        channel = (await ExpressionNode(self.interpreter.next_token()).create()).value
        if type(channel) == int:
            channel = await self.interpreter.bot.fetch_channel(int(channel))
        else:
            channel = channel.name
        self.value = MessageClass(await channel.send(message))
        return self

