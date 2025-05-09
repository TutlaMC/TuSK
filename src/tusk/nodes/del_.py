from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode
from tusk.discord_classes import to_discord_object
import os

class DelNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        nxt_tkn = self.interpreter.next_token()
        if nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "file":
            os.remove((await ExpressionNode(self.interpreter.next_token()).create()).value)
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "folder":
            os.rmdir((await ExpressionNode(self.interpreter.next_token()).create()).value)
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "variable":
            self.interpreter.data["vars"].pop([self.interpreter.next_token().value])
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "message":
            message = (await ExpressionNode(self.interpreter.next_token()).create()).value
            print(type(message))
            message = await to_discord_object(self.interpreter.bot, message, "message")
            print(type(message))
            await message.delete()
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "channel":
            channel = (await ExpressionNode(self.interpreter.next_token()).create()).value
            channel = await to_discord_object(self.interpreter.bot, channel, "channel")
            await channel.delete()
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "category":
            category = (await ExpressionNode(self.interpreter.next_token()).create()).value
            category = await to_discord_object(self.interpreter.bot, category, "category")
            await category.delete()
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "emoji":
            emoji = (await ExpressionNode(self.interpreter.next_token()).create()).value
            emoji = await to_discord_object(self.interpreter.bot, emoji, "emoji")
            await emoji.delete()
        else:
            raise Exception(f"Expected KEYWORD:file | KEYWORD:folder | KEYWORD:variable | KEYWORD:message | KEYWORD:channel | KEYWORD:category, got {nxt_tkn.value}")
        return self
