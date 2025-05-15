from tusk.node import Node
from tusk.token import Token
from tusk.nodes.expressions import ExpressionNode
from tusk.nodes.base.name import NameNode
from tusk.variable import Variable, is_ordinal_number

class SetNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        name = self.interpreter.next_token()
        if is_ordinal_number(name):
            print("guh")
            n = is_ordinal_number(name)-1
            self.interpreter.expect_token("KEYWORD:item|KEYWORD:character")
            self.interpreter.expect_token("LOGIC:in")
            e = NameNode(self.interpreter.next_token())
            self.interpreter.expect_token("KEYWORD:to")
            e.value[n] = (await ExpressionNode(self.interpreter.next_token()).create()).value
        else:
            """
                        vname = name.value
                        to_set = self.interpreter.data["vars"]
                        while self.interpreter.get_next_token().type == "PROPERTY":
                            to_set = to_set[vname]
                            self.interpreter.next_token()
                            vname = self.interpreter.expect_token("IDENTIFIER").value
                            to_set = to_set.properties
            """
            n = (await NameNode(self.interpreter.current_token).create())

            self.interpreter.expect_token("KEYWORD:to")
            value = (await ExpressionNode(self.interpreter.next_token()).create()).value
            if isinstance(value, Variable):
                value.name = n.name
                n.location[n.name] = value
                self.interpreter.data["vars"]["it"] = value
                self.interpreter.data["vars"]["this"] = value
            else:
                n.location[n.name] = Variable(n.name,value)
                self.interpreter.data["vars"]["it"] = value
                self.interpreter.data["vars"]["this"] = value
                