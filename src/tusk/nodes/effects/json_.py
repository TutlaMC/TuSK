import json

from tusk.node import Node
from tusk.token import Token

class JsonNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter
        
    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        action = self.interpreter.next_token().value
        if action == "jsloads":
            e = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.value = json.loads(e)
        elif action == "jsdumps":
            e = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.value = json.dumps(e)
        elif action == "jsload":
            e = (await ExpressionNode(self.interpreter.next_token()).create()).value
            with open(e, "r") as f:
                self.value = json.load(f)
        elif action == "jsave":
            e = (await ExpressionNode(self.interpreter.next_token()).create()).value
            with open(e, "w") as f:
                js = (await ExpressionNode(self.interpreter.next_token()).create()).value
                js = json.loads(js)
                json.dump(js, f)
        else:
            self.interpreter.error("JSONError (tson rly)", f"Invalid JSON action: {action}")
        return self