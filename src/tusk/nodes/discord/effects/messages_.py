from tusk.node import Node
from tusk.token import Token

from tusk.discord_classes import MessageClass, to_discord_object


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
        try:    
            channel = await to_discord_object(self.interpreter.bot, channel, "channel")
        except UnboundLocalError:
            self.interpreter.error("NoChannelProvided",f"You havent provided a channel to send the message to!",notes=["Possible Fix: add `to your_channel_here` to the send the message. your_channel_here should be a channel not a channel name (tusk will atempt to find it but in most cases it will fail)"])
        self.value = MessageClass(await channel.send(message))
        return self

class EditNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
        
    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        message = (await ExpressionNode(self.interpreter.next_token()).create()).value
        message:discord.Message = await to_discord_object(self.interpreter.bot, message, "message")
        self.interpreter.expect_token("KEYWORD:to")
        text = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.value = await message.edit(content=text)
        self.value = MessageClass(self.value)
        return self
    

