from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode


class ReturnNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.type="1en"
        self.token = token

    async def create(self):
        self.interpreter.return_value = (await ExpressionNode(self.interpreter.next_token()).create()).value
        return self

        
