from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode


class ReturnNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.type="1en"


        self.interpreter.return_value = ExpressionNode(self.interpreter.next_token()).value

        
