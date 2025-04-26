from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

class InputNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        txt = ""
        if self.interpreter.get_next_token().type == "STRING":
            txt = self.interpreter.next_token().value
        self.value = input(txt)