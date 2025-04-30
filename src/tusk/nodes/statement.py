import time, asyncio

from tusk.node import Node
from tusk.token import Token
from tusk.variable import  Variable
from tusk.nodes.base.if_node import *
from tusk.nodes.base.function import *
from tusk.nodes.base.loops import WhileNode, LoopNode
from tusk.nodes.del_ import DelNode
from tusk.nodes.expressions import *

class StatementNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True


        if token.type in ["KEYWORD", "IDENTIFIER","STRUCTURE","EFFECT","LEFT_CURLY","NUMBER","STRING"]:
            if token.type == "EFFECT":
                if token.value == "print":
                    e = ExpressionNode(self.interpreter.next_token())
                    print(e.value)
                elif token.value == "set":
                    from tusk.nodes.effects.set import SetNode
                    SetNode(token)
                elif token.value == "wait":
                    time.sleep(ExpressionNode(self.interpreter.next_token()).value)
                elif token.value == "delete":
                    DelNode(token)
                elif self.value.value == "write":
                    from tusk.nodes.effects.fs import WriteNode
                    WriteNode(self.value)
                elif self.value.value == "rename":
                    from tusk.nodes.effects.fs import RenameNode
                    RenameNode(self.value)
            elif token.type == "STRUCTURE":
                if token.value == "if":
                    IfNode(self.interpreter.next_token())
                elif token.value == "function":
                    FunctionNode(self.interpreter.next_token())
                elif token.value == "while":
                    WhileNode(self.interpreter.next_token())
                elif token.value == "loop":
                    LoopNode(self.interpreter.next_token())
            
            elif token.type == "IDENTIFIER":
                ExpressionNode(self.interpreter.current_token)
            elif token.type == "KEYWORD":
                ExpressionNode(self.interpreter.current_token)
            elif token.type in ["LEFT_CURLY","NUMBER","STRING"]:
                ExpressionNode(self.interpreter.current_token)
            else: raise Exception(f"Unexpected Token: {token}")
        else: raise Exception(f"Expected KEYWORD | VALID_IDENTIFIER | STRUCTURE, got {self.interpreter.current_token.type} @tusk {self.interpreter.current_token.value}{token}")


        self.type="1en"
