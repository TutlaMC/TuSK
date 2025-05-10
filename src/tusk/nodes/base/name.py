from tusk.token import Token
from tusk.node import Node
from tusk.variable import Variable, istusk
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
            self.interpreter.debug_msg(self.interpreter.current_token, "<- name (node) property start")
            while self.interpreter.get_next_token().type == "PROPERTY":
                self.interpreter.next_token() 
                self.name = self.interpreter.next_token().value
                if not self.name in self.location:break
                if self.interpreter.get_next_token().type == "PROPERTY":
                    self.location = self.location[self.name].properties
                else: break
            self.interpreter.debug_msg(self.interpreter.current_token, "<- name (node) property end")
                

        if self.name in self.location: 
            if type(self.location[self.name]) != Variable:
                self.value = self.location[self.name]
            elif istusk(self.location[self.name]):
                self.value = self.location[self.name].get_value()
        self.interpreter.debug_msg("name", "<- name (node) end")
        return self
        

def setter(name,value,interpreter):
    location = interpreter.data["vars"]
    if is_tusk_object(value):
        location[name] = value
    else:
        location[name] = Variable(name,value)
    return location[name]