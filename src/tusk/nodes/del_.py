from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode
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
        else:
            raise Exception(f"Expected KEYWORD:file | KEYWORD:folder | KEYWORD:variable, got {nxt_tkn.value}")
        return self
