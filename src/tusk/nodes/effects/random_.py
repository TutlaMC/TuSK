from tusk.node import Node
from tusk.token import Token
import random
class RandomNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        typ = self.interpreter.next_token()
        if typ.value == "number":
            self.interpreter.expect_token("KEYWORD:between")
            num1 = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.interpreter.expect_token("KEYWORD:and")
            num2 = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.value = random.randint(num1, num2)
        elif typ.value == "item":
            self.interpreter.expect_token("KEYWORD:of")
            items = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.value = random.choice(items)
        elif typ.value == "character":
            if self.interpreter.get_next_token().value == "of":
                self.interpreter.next_token()
                characters = (await ExpressionNode(self.interpreter.next_token()).create()).value
                self.value = random.choice(characters)
            else:
                characters = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=[]{}|;:,.<>?~"
                characters = characters+characters.upper()
                self.value = random.choice(characters)
        elif typ.value == "letter":
            self.value = random.choice("abcdefghijklmnopqrstuvwxyz")
        else:
            self.interpreter.error("InvalidRandomType", f"Invalid random type: {typ.value}")
            
        return self
