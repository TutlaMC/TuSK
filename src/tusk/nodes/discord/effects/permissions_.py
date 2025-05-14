from tusk.node import Node
from tusk.token import Token
from tusk.discord_classes import *
from tusk.lexer import PermissionNames

class AllowNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        """
        Allow a user/role a permission (in channel/category is optional)
        """

        from tusk.nodes.expressions import ExpressionNode

        allow = True
        if self.token.value == "disallow":
            allow = False

        role_or_user = self.interpreter.expect_token("KEYWORD:user|KEYWORD:role").value

        obj = (await ExpressionNode(self.interpreter.next_token()).create()).value
        obj = await to_discord_object(self.interpreter.bot, obj, to_type=role_or_user)
        self.interpreter.expect_token("KEYWORD:to")

        permission = self.interpreter.next_token().value

        
        if role_or_user == "role" and type(obj) != discord.Role:
            self.interpreter.error("InvalidObject",f"Invalid object: {obj}")
        elif role_or_user == "user" and type(obj) != discord.Member:
            self.interpreter.error("Invalid user", f"The user `{self.interpreter.next_token().value}` is NOT a member of a server. Please use a valid user.",notes=["Possible Fix: Try using `get` and provide a channel/server id to search the user or use a reference user like event_user where event_user is a member of a server","Possible Cause: Another probabl cause could be that you used event_user but the event_channel was a DM","Are you seeing this again? The first time you rpboably gave the user id or name and then corrected it to get but forgot to provide a channel or guild, so its a USER instead of a MEMBER, in rookie terms its as if your checking the user's profile from the friends tab, you can't see the roles of a specific server in there."])
        if permission not in PermissionNames:
            self.interpreter.error("InvalidPermission",f"Invalid permission: {permission}")

        # From here it just gets confusing
        if self.interpreter.get_next_token().value == "in":
            self.interpreter.next_token() # skip in
            room_type = self.interpreter.expect_token("KEYWORD:channel|KEYWORD:category|KEYWORD:server").value
            room = (await ExpressionNode(self.interpreter.next_token()).create()).value
            room = await to_discord_object(self.interpreter.bot, room, to_type=room_type)
        else:
            if type(obj) != discord.Role:
                self.interpreter.error("InvalidObject",f"You cannot set permissions for a member in a server, you can only change a role's permissions. Please use a role instead, try using `[user]'s top_role`",notes=["Rookie Terms: Think of how you could change a user's permission in a server, yes you can't- unless your changing their permission in a channel or category. If you go to server settings theres only a tab for roles you could give a user a role instead"])
            room = obj

        if self.interpreter.get_next_token().value == "beacause":
            self.interpreter.next_token() # skip because
            reason = self.interpreter.next_token().value
        else:
            reason = None

        permissions = discord.PermissionOverwrite()
        permissions.__setattr__(permission, allow)
        if type(room) != discord.Guild:
            await room.set_permissions(obj, overwrite=permissions,reason=reason)
        else:
            await room.edit(permissions=permissions,reason=reason)
        return ChannelClass(room)



            
            
