from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode

import os

class ReadNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        file = ExpressionNode(self.interpreter.next_token()).value
        with open(file, "r") as f:
            self.value = f.read()

class WriteNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter


        txt = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("KEYWORD:to")
        with open(ExpressionNode(self.interpreter.next_token()).value, "w") as f:
            self.value = f.write(txt)

class RenameNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        old_name = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("KEYWORD:to")
        new_name = ExpressionNode(self.interpreter.next_token()).value
        os.rename(old_name, new_name)
        self.value = new_name

