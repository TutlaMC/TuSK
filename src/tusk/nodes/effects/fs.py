from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode

import os

class ReadNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        with open((await ExpressionNode(self.interpreter.next_token()).create()).value, "r") as f:
            self.value = f.read()
        return self

class WriteNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        text = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:to")
        file = (await ExpressionNode(self.interpreter.next_token()).create()).value
        with open(file, "w") as f:
            f.write(text)
        return self

class RenameNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        old_name = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:to")
        new_name = (await ExpressionNode(self.interpreter.next_token()).create()).value
        os.rename(old_name, new_name)
        self.value = new_name
        return self

