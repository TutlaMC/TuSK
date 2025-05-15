

class Token:
    def __init__(self, type_, value, interpreter):
        from tusk.interpreter import Interpreter
        self.type = type_
        self.value = value
        self.interpreter: Interpreter = interpreter

    def __repr__(self):
        return f'({self.type}:{self.value})'