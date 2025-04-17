import time

from tusk.node import Node
from tusk.token import Token
from tusk.variable import  Variable
from tusk.nodes.base.if_node import *
from tusk.nodes.base.function import *
from tusk.nodes.base.loops import WhileNode, LoopNode


class StatementNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True


        if token.type in ["KEYWORD", "IDENTIFIER","STRUCTURE","EFFECT"]:
            if token.type == "EFFECT":
                if token.value == "print":
                    e = ExpressionNode(self.interpreter.next_token())
                    print(e.value)
                elif token.value == "set":
                    name = self.interpreter.next_token()
                    if is_ordinal_number(name):
                        n = is_ordinal_number(name)-1
                        self.interpreter.next_token()
                        self.interpreter.expect_token("LOGIC:in")
                        e = self.interpreter.data["vars"][self.interpreter.next_token().value] # TODO: Make this NameNode
                        self.interpreter.expect_token("KEYWORD:to")
                        e.value[n] = ExpressionNode(self.interpreter.next_token()).value
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
                        n = NameNode(self.interpreter.current_token)


                        self.interpreter.expect_token("KEYWORD:to")
                        value = ExpressionNode(self.interpreter.next_token()).value
                        n.location[n.name] = Variable(n.name,value)
                elif token.value == "wait":
                    time.sleep(ExpressionNode(self.interpreter.next_token()).value)
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
            else: raise Exception(f"Unexpected Token: {token}")
        else: raise Exception(f"Expected KEYWORD | VALID_IDENTIFIER | STRUCTURE, got {self.interpreter.current_token.type} @tusk {self.interpreter.current_token.value}{token}")


        self.type="1en"
