from tusk.token import Token
from tusk.node import Node
from tusk.variable import Variable

class NameNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        interpreter = token.interpreter

        self.name = token.value # variable name
        self.value = None
        
        self.location = token.interpreter.data["vars"]
        

        if interpreter.get_next_token().type == "PROPERTY":
            self.location = self.location[self.name].properties
            while interpreter.get_next_token().type == "PROPERTY":
                interpreter.next_token() 
                self.name = interpreter.expect_token("IDENTIFIER").value
                if not self.name in self.location:break
                if interpreter.get_next_token().type == "PROPERTY":
                    self.location = self.location[self.name].properties
                else: break
                

        if self.name in self.location: 
            self.value = self.location[self.name] if type(self.location[self.name]) != Variable else self.location[self.name].value
        