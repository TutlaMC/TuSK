from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

import subprocess
import io
import sys


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
        
        code = str(ExpressionNode(self.interpreter.next_token()).value)
        
        if capture:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            
            try:
                exec(code)
                self.value = new_stdout.getvalue()
            except Exception as e:
                self.value = str(e)
            finally:
                sys.stdout = old_stdout
            
        else:
            exec(code)
            self.value = None

