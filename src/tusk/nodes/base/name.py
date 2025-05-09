from tusk.token import Token
from tusk.node import Node
from tusk.variable import Variable
from tusk.discord_classes import is_tusk_object
class NameNode(Node):
    def __init__(self, token:Token):
        self.interpreter = token.interpreter
        interpreter = token.interpreter
        self.token = token

        self.name = token.value # variable name
        self.value = None
        
        self.location = token.interpreter.data["vars"]
        

    async def create(self):
        self.interpreter.debug_msg(self.token, "<- name (node) start")
        if self.interpreter.get_next_token().type == "PROPERTY":
            self.location = self.location[self.name].properties
            self.interpreter.debug_msg(self.interpreter.get_next_token(), "<- name (node) property start")
            while self.interpreter.get_next_token().type == "PROPERTY":
                self.interpreter.next_token() 
                self.name = self.interpreter.expect_token("IDENTIFIER").value
                if not self.name in self.location:break
                if self.interpreter.get_next_token().type == "PROPERTY":
                    self.location = self.location[self.name].properties
                else: break
                

        if self.name in self.location: 
            self.value = self.location[self.name] if type(self.location[self.name]) != Variable else (self.location[self.name].value if type(self.location[self.name].value) != Variable else self.location[self.name].value.value)
        self.interpreter.debug_msg("name", "<- name (node) end")
        return self
        

def setter(name,value,interpreter):
    location = interpreter.data["vars"]
    if is_tusk_object(value):
        location[name] = value
    else:
        location[name] = Variable(name,value)
    return location[name]