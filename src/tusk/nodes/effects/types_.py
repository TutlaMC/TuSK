from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode
from tusk.variable import types_
class ConvertNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import types_
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        val = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:to")
        self.value = types_[self.interpreter.next_token().value.upper()](val)
        return self