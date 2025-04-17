class Token:
    def __init__(self, type_, value, interpreter):
        self.type = type_
        self.value = value
        self.interpreter = interpreter

    def __repr__(self):
        return f'({self.type}:{self.value})'