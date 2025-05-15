from tusk.node import Node
from tusk.token import Token
from tusk.discord_classes import *
class TimeoutNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        user = (await ExpressionNode(self.interpreter.next_token()).create()).value
        user:discord.Member|discord.User = await to_discord_object(self.interpreter.bot,user,"user")
        

        self.interpreter.expect_token("KEYWORD:for")
        time = (await ExpressionNode(self.interpreter.next_token()).create()).value
        if type(time) != int:
            self.interpreter.error("InvalidTime",f"Time {time} is not an integer")
        
        if self.interpreter.is_token("KEYWORD:because"):
            self.interpreter.next_token()
            reason = (await ExpressionNode(self.interpreter.next_token()).create()).value
        else:
            reason = None

        if user is None:
            self.interpreter.error("UserNotFound",f"User {user} not found")
        await user.timeout(reason=reason,until=time)

class KickNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        user = (await ExpressionNode(self.interpreter.next_token()).create()).value
        user:discord.Member|discord.User = await to_discord_object(self.interpreter.bot,user,"user")
        if self.interpreter.is_token("KEYWORD:because"):
            self.interpreter.next_token()
            reason = (await ExpressionNode(self.interpreter.next_token()).create()).value
        else:
            reason = None
        if user is None:
            self.interpreter.error("UserNotFound",f"User {user} not found")
        await user.kick(reason=reason)

class BanNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        user = (await ExpressionNode(self.interpreter.next_token()).create()).value
        user:discord.Member|discord.User = await to_discord_object(self.interpreter.bot,user,"user")
        if self.interpreter.is_token("KEYWORD:because"):
            self.interpreter.next_token()
            reason = (await ExpressionNode(self.interpreter.next_token()).create()).value
        else:
            reason = None
        if user is None:
            self.interpreter.error("UserNotFound",f"User {user} not found")
        await user.ban(reason=reason)

class UnbanNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        user = (await ExpressionNode(self.interpreter.next_token()).create()).value
        user:discord.Member|discord.User = await to_discord_object(self.interpreter.bot,user,"user")
        self.interpreter.expect_token("LOGIC:in")
        guild = (await ExpressionNode(self.interpreter.next_token()).create()).value
        guild:discord.Guild = await to_discord_object(self.interpreter.bot,guild,"guild")
        if self.interpreter.is_token("KEYWORD:because"):
            self.interpreter.next_token()
            reason = (await ExpressionNode(self.interpreter.next_token()).create()).value
        else:
            reason = None
        if user is None:
            self.interpreter.error("UserNotFound",f"User {user} not found")
        await guild.unban(user,reason=reason)
        