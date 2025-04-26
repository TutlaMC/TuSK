from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

import subprocess


class ShellNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import types_
        self.interpreter = token.interpreter
        
        capture = False
        if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "capture":
            self.interpreter.next_token()
            capture = True
        
        if capture:
            self.value = subprocess.run(str(ExpressionNode(self.interpreter.next_token()).value), shell=True)
        else: 
            self.value = subprocess.check_output(str(ExpressionNode(self.interpreter.next_token()).value), shell=True, text=True)


class PythonNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import types_
        self.interpreter = token.interpreter
        
        capture = False
        if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "capture":
            self.interpreter.next_token()
            capture = True
        
        if capture:
            self.value = subprocess.run(str(ExpressionNode(self.interpreter.next_token()).value), shell=True)
        else: 
            self.value = subprocess.check_output(str(ExpressionNode(self.interpreter.next_token()).value), shell=True, text=True)


