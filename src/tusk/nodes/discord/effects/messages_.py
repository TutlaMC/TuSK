from tusk.node import Node
from tusk.token import Token

from tusk.discord_classes import *


import asyncio
import discord

class MessageNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        message = (await ExpressionNode(self.interpreter.next_token()).create()).value
        if self.token.value == "edit":
            message = await to_discord_object(self.interpreter.bot, message, "message")
            self.interpreter.expect_token("KEYWORD:to")
            content = (await ExpressionNode(self.interpreter.next_token()).create()).value
            
        nfiles = []
        nembeds = []
        delete_after = None
        if self.interpreter.get_next_token().value == "with":
            self.interpreter.next_token()
            while self.interpreter.get_next_token().value in ["files","file","embed","attachment","attachments","delete_after"]:
                tkn = self.interpreter.next_token()
                self.interpreter.expect_token("KEYWORD:as")
                if tkn.value in ["attachment","attachments","files","file"]:
                    files = (await ExpressionNode(self.interpreter.next_token()).create()).value
                    if type(files) != list:
                        files = [files]
                    
                    
                    for file in files:
                        if type(file) == str:
                            file = discord.File(file)
                        elif type(file) == AttachmentClass:
                            file = file.properties["python"]
                        elif type(file) == discord.File:
                            pass
                        elif type(file) == discord.Attachment:
                            file = discord.File(file.url,file.filename)
                        else:
                            self.interpreter.error("InvalidFile",f"Invalid file type: {type(file)}")
                        nfiles.append(file)
                elif tkn.value in ["embed","embeds"]:
                    pass #coming soon
                elif tkn.value == "delete_after":
                    self.interpreter.next_token()
                    delete_after = (await ExpressionNode(self.interpreter.next_token()).create()).value # in seconds
                    if type(delete_after) != int:
                        self.interpreter.error("InvalidDeleteAfter",f"Invalid delete after time: {type(delete_after)}")
                
                if self.interpreter.get_next_token().value != "and":
                    break
                else:
                    self.interpreter.next_token()

        if self.token.value == "send":
            self.interpreter.expect_token("KEYWORD:to",notes=["Possible Fix: add `to your_channel_here` to the send the message. your_channel_here should be a channel not a channel name (tusk will atempt to find it but in most cases it will fail)"])
            channel = (await ExpressionNode(self.interpreter.next_token()).create()).value
            try:    
                channel = await to_discord_object(self.interpreter.bot, channel, "channel")
            except UnboundLocalError:
                try:
                    channel = await to_tusk_object(self.interpreter.bot, channel, "user")
                except UnboundLocalError:
                    self.interpreter.error("NoChannelOrUserProvided",f"You havent provided a channel or user to send the message to!",notes=["Possible Fix: add `to your_channel_here` to the send the message. your_channel_here should be a channel not a channel name (tusk will atempt to find it but in most cases it will fail)"])
            
            self.value = MessageClass(await channel.send(message,files=nfiles,delete_after=delete_after))
        else:
            self.value = MessageClass(await message.edit(content=content,attachments=nfiles))
        return self
"""
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
"""