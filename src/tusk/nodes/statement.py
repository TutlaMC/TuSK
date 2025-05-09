import time, asyncio

from tusk.node import Node
from tusk.token import Token
from tusk.variable import  Variable
from tusk.nodes.base.if_node import *
from tusk.nodes.base.function import *
from tusk.nodes.base.loops import WhileNode, LoopNode
from tusk.nodes.del_ import DelNode
from tusk.nodes.expressions import *
from tusk.nodes.base.return_node import ReturnNode
from tusk.nodes.effect import EffectNode
class StatementNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.token = token

    async def create(self):
        self.interpreter.debug_msg(self.token, "<- stmt (node) token")
        if self.interpreter.end_found:
            return False
        if self.token.type in ["KEYWORD", "IDENTIFIER","STRUCTURE","EFFECT","LEFT_CURLY","NUMBER","STRING"]:
            if self.token.type == "EFFECT":
                await EffectNode(self.token).create()
            elif self.token.type == "STRUCTURE":
                if self.token.value == "if":
                    await IfNode(self.interpreter.next_token()).create()
                elif self.token.value == "function":
                    await FunctionNode(self.interpreter.next_token()).create()
                elif self.token.value == "while":
                    await WhileNode(self.interpreter.next_token()).create()
                elif self.token.value == "loop":
                    await LoopNode(self.interpreter.next_token()).create()
                    
                elif self.token.value == "on":
                    from tusk.nodes.discord.base.on import OnNode
                    await OnNode(self.token).create()
            elif self.token.type == "IDENTIFIER":
                await ExpressionNode(self.token).create()
            elif self.token.type == "KEYWORD":
                await ExpressionNode(self.token).create()
            elif self.token.type in ["LEFT_CURLY","NUMBER","STRING"]:
                await ExpressionNode(self.token).create()
            elif self.token.type == "BREAKSTRUCTURE":
                await ReturnNode(self.token).create()
            else: self.interpreter.error("UnexpectedToken", f"Expected KEYWORD | VALID_IDENTIFIER | STRUCTURE, got {self.interpreter.current_token.type} @tusk {self.interpreter.current_token.value}{self.token}", notes=["Possible Fix: Recheck code with documentation, you might have missed a keyword at position"])

        else: self.interpreter.error("UnexpectedToken", f"Expected KEYWORD | VALID_IDENTIFIER | STRUCTURE, got {self.interpreter.current_token.type} @tusk {self.interpreter.current_token.value}{self.token}", notes=["Possible Fix: Recheck code with documentation, you might have missed a keyword at position"])

        self.type="1en"
        self.interpreter.debug_msg(self.interpreter.current_token, "<- stmt (node) end\n\n")
        return self