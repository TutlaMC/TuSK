from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

from tusk.discord_classes import to_tusk_object, to_discord_object

import discord

class GetNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        e = self.interpreter.expect_token("KEYWORD:item|KEYWORD:character|KEYWORD:channel|KEYWORD:server|KEYWORD:user|KEYWORD:message|KEYWORD:role|KEYWORD:emoji|STRING")
        if e.type == "STRING":
            self.interpreter.expect_token("LOGIC:in")
            list_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
            if type(list_) == str:
                self.value = list_.index(e.value)
            elif type(list_) == list:
                self.value = list_.index(e.value)
            elif type(list_) == dict:
                self.value = list_[e.value]
            else:
                raise Exception(f"get requires <string> or <list> or <dict> not {type(list_)}")
        elif e.value in ["item","character"]:
            self.interpreter.expect_token("KEYWORD:number")
            index = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.interpreter.expect_token("KEYWORD:of")
            list_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
            if type(list_) == str:
                self.value = list_[int(index)-1]
            elif type(list_) == list:
                self.value = list_[int(index)-1]
            else:
                raise Exception(f"get requires <string> or <list> not {type(list_)}")
            return self
        elif e.value in ["channel","server","member","user","message","role","emoji","category"]:
            bot:discord.Client = self.interpreter.bot
            name = (await ExpressionNode(self.interpreter.next_token()).create()).value
            if e.value == "channel":
                from tusk.discord_classes import ChannelClass
                if type(name) == int:
                    self.value = ChannelClass(await self.interpreter.bot.fetch_channel(int(name)))
                elif type(name) == str:
                    for guild in self.interpreter.bot.guilds:
                        channel = discord.utils.get(guild.channels, name=name)
                        if channel:
                            self.value = ChannelClass(channel)
                            break
                    else:
                        self.interpreter.error("ChannelNotFound", f"Channel with name '{name}' not found")
                else:
                    self.value = to_tusk_object(self.interpreter.bot, name, "channel")
            elif e.value == "server":
                from tusk.discord_classes import GuildClass
                if type(name) == int:
                    self.value = GuildClass(await self.interpreter.bot.fetch_guild(int(name)))
                elif type(name) == str:
                    for guild in self.interpreter.bot.guilds:
                        if guild.name.lower() == name.lower():
                            self.value = GuildClass(guild)
                            break
                    else:
                        self.interpreter.error("GuildNotFound", f"Guild with name '{name}' not found")
            elif e.value == "user":
                    from tusk.discord_classes import UserClass
                    if type(name) == int:
                        self.value = UserClass(await self.interpreter.bot.fetch_user(int(name)))
                    elif type(name) == str:
                        for user in self.interpreter.bot.users:
                            if user.name.lower() == name.lower():
                                self.value = UserClass(user)
                                break
                        else:
                            self.interpreter.error("UserNotFound", f"User with name '{name}' not found")
            elif e.value == "member":
                from tusk.discord_classes import UserClass
                self.interpreter.expect_token("LOGIC:in")
                server = (await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "guild"))
                if type(name) == int:
                    self.value = UserClass(await server.fetch_member(int(name)))
                elif type(name) == str:
                    for member in server.members:
                        if member.name.lower() == name.lower():
                            self.value = UserClass(member)
                            break
                    else:
                        self.interpreter.error("MemberNotFound", f"Member with name '{name}' not found")
                    
            elif e.value == "message":
                    from tusk.discord_classes import MessageClass
                    if type(name) == int:
                        if self.interpreter.get_next_token().type == "LOGIC" and self.interpreter.get_next_token().value == "in":
                            self.interpreter.expect_token("KEYWORD:channel")
                            channel = (await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "channel"))
                            self.value = MessageClass(await channel.fetch_message(int(name)))
                        else:
                            for channel in self.interpreter.bot.channels:
                                message = discord.utils.get(channel.messages, content=name)
                                if message:
                                    self.value = MessageClass(message)
                                    break
                            else:
                                self.interpreter.error("MessageNotFound", f"Message with id '{name}' not found")
                    elif type(name) == str:
                        for channel in self.interpreter.bot.channels:
                            message = discord.utils.get(channel.messages, content=name)
                            if message:
                                self.value = MessageClass(message)
                                break
                        else:
                            self.interpreter.error("MessageNotFound", f"Message with content '{name}' not found")

            elif e.value == "role":
                    from tusk.discord_classes import RoleClass
                    if type(name) == int:
                        self.interpreter.expect_token("LOGIC:in")
                        server = (await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "guild"))
                        for role in server.roles:
                            if role.id == name:
                                self.value = RoleClass(role)
                                break
                        else:
                            self.interpreter.error("RoleNotFound", f"Role with id '{str(name)}' not found")
                    elif type(name) == str:
                        self.interpreter.expect_token("LOGIC:in")
                        server = (await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "guild"))
                        for role in server.roles:
                            if role.name.lower() == name.lower():
                                self.value = RoleClass(role)
                                break
                        else:
                            self.interpreter.error("RoleNotFound", f"Role with name '{name}' not found")
            elif e.value == "emoji":
                    from tusk.discord_classes import EmojiClass
                    if type(name) == int:
                        self.interpreter.expect_token("LOGIC:in")
                        server = (await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "guild"))
                        for emoji in server.emojis:
                            if emoji.id == name:
                                self.value = EmojiClass(emoji)
                                break
                        else:
                            self.interpreter.error("EmojiNotFound", f"Emoji with id '{str(name)}' not found")
                    elif type(name) == str:
                        self.interpreter.expect_token("LOGIC:in")
                        server = (await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "guild"))
                        for emoji in server.emojis:
                            if emoji.name.lower() == name.lower():
                                self.value = EmojiClass(emoji)
                                break
                        else:
                            self.interpreter.error("EmojiNotFound", f"Emoji with name '{name}' not found")
                            

            else:
                raise Exception(f"get requires <int> or <str> not {type(name)}")
        return self