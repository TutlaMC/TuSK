from tusk.interpreter import *

with open("scripts/test.tusk", "r") as f:
    code = f.read()

TuskTestInterpreter = Interpreter()
TuskTestInterpreter.setup(text=code)
TuskTestInterpreter.compile()