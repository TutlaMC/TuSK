from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode
import os

class DelNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        nxt_tkn = self.interpreter.next_token()
        if nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "file":
            os.remove(ExpressionNode(self.interpreter.next_token()).value)
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "folder":
            os.rmdir(ExpressionNode(self.interpreter.next_token()).value)
        elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "variable":
            self.interpreter.data["vars"].pop([self.interpreter.next_token().value])
        else:
            raise Exception(f"Expected KEYWORD:file | KEYWORD:folder | KEYWORD:variable, got {nxt_tkn.value}")
