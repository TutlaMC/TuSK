from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

class InputNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        txt = ""
        self.value = input(ExpressionNode(self.interpreter.next_token()).value)