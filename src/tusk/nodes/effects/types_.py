from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

class ConvertNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import types_
        self.interpreter = token.interpreter
        
        val = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("KEYWORD:to")
        self.value = types_[self.interpreter.next_token().value](val)