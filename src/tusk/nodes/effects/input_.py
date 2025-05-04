from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

class InputNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        txt = ""
        self.value = input((await ExpressionNode(self.interpreter.next_token()).create()).value)
        return self