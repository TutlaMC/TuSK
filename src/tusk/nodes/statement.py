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
                if self.token.value == "print":
                    e = await ExpressionNode(self.interpreter.next_token()).create()
                    print(e.value)
                elif self.token.value == "set":
                    from tusk.nodes.effects.set import SetNode
                    await SetNode(self.token).create()
                elif self.token.value == "wait":
                    try:
                        time.sleep((await ExpressionNode(self.interpreter.next_token()).create()).value)
                    except KeyboardInterrupt as e:
                        self.interpreter.error("KeyboardInterrupt", "User cancelled wait", [f"You pressed Ctrl+C"])
                elif self.token.value == "delete":
                    await DelNode(self.token).create()
                elif self.token.value == "write":
                    from tusk.nodes.effects.fs import WriteNode
                    await WriteNode(self.token).create()
                elif self.token.value == "rename":
                    from tusk.nodes.effects.fs import RenameNode
                    await RenameNode(self.token).create()
                

                
                else:
                    await ExpressionNode(self.token).create()
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