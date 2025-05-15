import discord
from tusk.node import Node
from tusk.token import Token
from tusk.discord_classes import to_discord_object
class ChangeNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter
        
    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        
        to_change = self.interpreter.next_token().value
        self.interpreter.expect_token("LOGIC:of")
        context_type = self.interpreter.expect_token("KEYWORD:channel|KEYWORD:server|KEYWORD:category|KEYWORD:role|KEYWORD:user").value

        if context_type == "channel":
            context = await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "channel")
        elif context_type == "server":
            context = await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "guild")
        elif context_type == "category":
            context = await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "category")
        elif context_type == "role":
            context = await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "role")
        elif context_type == "user":
            context:discord.Member|discord.User = await to_discord_object(self.interpreter.bot, (await ExpressionNode(self.interpreter.next_token()).create()).value, "user")
        else:
            self.interpreter.error("InvalidContext",f"You provided {context_type}. Try providing a valid context (read docs)")

        self.interpreter.expect_token("LOGIC:to")
        new_value = await ExpressionNode(self.interpreter.next_token()).create()
        new_value = new_value.value

        if self.interpreter.get_next_token().value == "because":
            self.interpreter.next_token()
            reason = (await ExpressionNode(self.interpreter.next_token()).create()).value
        else:
            reason = None
        
        if to_change == "name":
            await context.edit(name=new_value, reason=reason)
        elif to_change == "topic":
            await context.edit(topic=new_value, reason=reason)
        elif to_change == "slowmode":
            await context.edit(slowmode_delay=new_value, reason=reason)
        elif to_change == "rate_limit":
            await context.edit(rate_limit_per_user=new_value, reason=reason)
        elif to_change == "position":
            await context.edit(position=new_value, reason=reason)
        elif to_change == "sync_permissions":
            await context.edit(sync_permissions=new_value, reason=reason)
        elif to_change == "category":
            if new_value is None:
                await context.edit(category=None, reason=reason)
            else:
                new_value = await to_discord_object(self.interpreter.bot, new_value, "category")
                if type(new_value) == discord.CategoryChannel:
                    await context.edit(category=new_value, reason=reason)
                else:
                    self.interpreter.error("Invalid category",f"You provided {new_value}. Try providing a valid category")
        elif to_change == "nsfw":
            await context.edit(nsfw=new_value, reason=reason)
        elif to_change == "slowmode":
            await context.edit(slowmode_delay=new_value, reason=reason)
        elif to_change == "color":
            await context.edit(color=new_value, reason=reason)
        elif to_change == "mentionable":
            await context.edit(mentionable=new_value, reason=reason)
        elif to_change == "nick":
            if type(context) == discord.Member:
                await context.edit(nick=new_value, reason=reason)
            else:
                self.interpreter.error("InvalidContext",f"You provided {context_type}. Try providing a valid context (read docs)")
        else:
            self.interpreter.error("InvalidChange",f"You provided {to_change}. Try providing a valid change (read docs)")

        
            
        
        