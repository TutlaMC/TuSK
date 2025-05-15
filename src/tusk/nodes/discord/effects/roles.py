from tusk.node import Node
from tusk.token import Token
from tusk.discord_classes import *

class RoleNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter
    
    async def create(self):
        """
        Grant/Revoke a role
        """

        from tusk.nodes.expressions import ExpressionNode

        if self.token.value == "grant":
            grant = True
        else:
            grant = False

        user = (await ExpressionNode(self.interpreter.next_token()).create()).value
        user = await to_discord_object(self.interpreter.bot, user, to_type="user")

        role = (await ExpressionNode(self.interpreter.next_token()).create()).value
        role = await to_discord_object(self.interpreter.bot, role, to_type="role")

        if type(user) == discord.Member and type(role) == discord.Role:
            if grant:
                try:
                    await user.add_roles(role)
                except Exception as e:
                    self.interpreter.error("InvalidContext", f"You don't have permission to add this role or the role is higher in hierarchy. Error: {e}")
            else:
                try:
                    await user.remove_roles(role)
                except Exception as e:
                    self.interpreter.error("InvalidContext", f"You don't have permission to remove this role or the role is higher in hierarchy. Error: {e}")
        else:
            self.interpreter.error("InvalidContext", "You can only grant/revoke roles to members. YOu provided an invalid role/member")
        
        self.interpreter.expect_token("KEYWORD:in")
        