from tusk.node import Node
from tusk.token import Token
from tusk.discord_classes import *

class ConditionNode(Node):
    def __init__(self,token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.token = token

        self.opposite = False

        if token.type == "LOGIC" and token.value=="not":
            self.opposite = True
            token = self.interpreter.next_token()
        
        self.token = token

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        tkn1 = await ExpressionNode(self.token).create()
        if self.token.interpreter.get_next_token().type == "LOGIC":
            operator = self.interpreter.next_token()
            tkn2 = await ConditionNode(self.interpreter.next_token()).create()
            if operator.value == "and" or operator.value == "&":
                if tkn1.value == True and tkn2.value == True: self.value = True
                else: self.value = False  
            elif operator.value == "or" or operator.value == "|":
                if tkn1.value == True or tkn2.value == True: self.value = True
                else: self.value = False  
            elif operator.value == "contains":
                if tkn2.value in tkn1.value: self.value = True
                else: self.value = False
            elif operator.value == "in":
                if tkn1.value in tkn2.value: self.value = True
                else: self.value = False
        elif self.token.value in ["can", "cannot"]:
            """
            To check if the user/role has a permission we'll need:
            - permission name
            - channel
            - user/role

            So the syntax will be : if user|role can|cannot permission_name in channel

            So we'll be recieving the permission name as a keyword/string/permission token, the user/role has to be a UserClass or a RoleClass and the channel could be an id/str/channelclass
            Then we'll just check with the channel if the member has the permission
            """
            if self.token.value == "cannot":
                self.opposite = True
            permission_name = self.interpreter.next_token().value # permission_name
            obj = tkn1.value # user|role
            self.interpreter.expect_token("LOGIC:in")
            channel = await ExpressionNode(self.interpreter.next_token()).create().value # channel

            ########## Converting everything to a discord object ##########
            channel = to_discord_object(self.interpreter.bot, channel, "channel")
            if not channel:
                self.interpreter.error("Invalid channel", f"The channel `{channel}` is invalid. Please use a valid channel.")
            
            if type(obj) == UserClass:
                obj = obj.properties["python"]
                if type(obj) != discord.Member:
                    self.interpreter.error("Invalid user", f"The user `{self.interpreter.next_token().value}` is NOT a member of a server. Please use a valid user.",notes=["Possible Fix: Try using `get` and provide a channel/server id to search the user or use a reference user like event_user where event_user is a member of a server","Possible Cause: Another probabl cause could be that you used event_user but the event_channel was a DM","Are you seeing this again? The first time you rpboably gave the user id or name and then corrected it to get but forgot to provide a channel or guild, so its a USER instead of a MEMBER, in rookie terms its as if your checking the user's profile from the friends tab, you can't see the roles of a specific server in there."])
            elif type(obj) == RoleClass:
                obj = obj.properties["python"]
            elif type(obj) in [discord.Member, discord.Role]:
                pass
            else:
                self.interpreter.error("Invalid user", f"The user/role `{str(obj)}` is invalid. Please use a valid user/role.",notes=["Possible Fix: Try using `get` and provide a channel/server id to search the user/role or use a reference user like event_user where event_user is a member of a server","Possible Cause: Another probabal cause could be that you used event_user but the event_channel was a DM"])
            
            ########## Checking if the user/role has the permission ##########
            if type(obj) == discord.Member:
                user = obj
                perms = await channel.permissions_for(user)
                if not user:
                    self.interpreter.error("Invalid user", f"The user `{self.interpreter.next_token().value}` is invalid. Please use a valid user.")
            elif type(obj) == discord.Role:
                role:discord.Role = obj
                perms:discord.Permissions = await channel.permissions_for(role)
            
            if permission_name in PermissionNames:
                print(getattr(perms, permission_name))
                if getattr(perms, permission_name):
                    self.value = True
                else:
                    self.value = False
            else:
                self.interpreter.error("Invalid permission name", f"The permission name `{permission_name}` is invalid. Please use a valid permission name.")
            
        else:
            self.value = tkn1.value
            self.type="1en"

        if self.opposite: 
            if self.value == True: self.value = False
            else: self.value = True

        

        return self