from tusk.node import Node
from tusk.token import Token
import os
class ImportNode(Node):
    def __init__(self, token: Token):
        self.token = token

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        from tusk.interpreter import Interpreter
        self.interpreter = self.token.interpreter

        file = (await ExpressionNode(self.interpreter.next_token()).create()).value
        if type(file) == str:
            file = file.replace(" ","").replace(".","/")
            if not file.endswith(".tusk"):
                file += ".tusk"
            if not file.startswith("scripts/"):
                file = "scripts/" + file
            elif not file.startswith("/scripts/"):
                file = "/scripts/" + file
            
            file_interpreter = Interpreter()
            file_interpreter.setup(file=file, bot=self.interpreter.bot)
            await file_interpreter.compile()
            try:
                self.interpreter.data["vars"].update(file_interpreter.data["vars"])
                self.interpreter.data["funcs"].update(file_interpreter.data["funcs"])
            except Exception as e:
                self.interpreter.error("ImportError", f"Error importing {file}, {e}", notes=["The script was not compiled correctly, fix the script before your import it"])

        else:
            self.interpreter.error("InvalidFile", f"Invalid file type, file should be a string path like 'library.tusk', 'example.tusk'")
        
            
            
            
