import re
import asyncio

from tusk.node import Node
from tusk.token import Token
from tusk.nodes.condition import *

from tusk.variable import Variable, types_

class FunctionNode(Node):
    def __init__(self, token: Token):
        
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusk.interpreter import Interpreter
        from tusk.nodes.statement import StatementNode
        from tusk.nodes.expressions import ExpressionNode
        self.name = self.token.value
        self.params = []

        """
        Each Param will look like:

        function add num1 num2:NUMBER

        num1 will be: num1 (takes in expression)
        num2 will be: NUMBER:num2
        """
        while self.interpreter.get_next_token().type in ["IDENTIFIER"]:
            param = self.interpreter.next_token().value
            if self.interpreter.get_next_token().type == "COLON":
                formed_param = f"{self.interpreter.next_token().interpreter.next_token().value}:{param}"
            else:
                formed_param = param
                
            self.params.append(formed_param)
        
        self.interpreter.data["funcs"][self.name] = [self.params]

        self.interpreter.expect_token("KEYWORD:that")

        self.function_interpreter = Interpreter()

        # puts all the tokens in here

        self.end_found = False

        self.tokens = []
        interal_stucture_count = 0

        
        while self.end_found != True:
            nxt_tkn = self.interpreter.get_next_token()

            if nxt_tkn.type == "STRUCTURE":
                interal_stucture_count += 1
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter = self.function_interpreter
                self.tokens.append(tkn_to_append)
            elif nxt_tkn.type == "ENDSTRUCTURE":
                if interal_stucture_count == 0:
                    self.interpreter.next_token()
                    self.end_found = True
                else:
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter = self.function_interpreter
                    self.tokens.append(tkn_to_append)
                    interal_stucture_count -= 1
            else:
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter = self.function_interpreter
                self.tokens.append(tkn_to_append)
        self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))


        self.function_interpreter.setup(tokens=self.tokens,data=self.interpreter.data,bot=self.interpreter.bot)
        self.interpreter.data["funcs"][self.name].append(self.function_interpreter)
        
    


        # Interpreter to interpret the function

        


        """
        self.if_loop("main")

        self.statement_complete = False


        
        if condition:
            self.function_interpreter.setup(tokens=self.statement["main"]["code"], data=self.interpreter.data).compile()
            self.statement_complete = True
        else:
            for name in self.statement:
                if self.statement_complete:
                    break
                if type(name) == int:
                    if self.statement[name]["condition"]:
                        self.function_interpreter.setup(tokens=self.statement[name]["code"], data=self.interpreter.data).compile()
                        self.statement_complete = True
        if self.statement_complete != True:
            if self.statement["else"]["code"] != None:
                self.function_interpreter.setup(tokens=self.statement["else"]["code"], data=self.interpreter.data).compile()
                self.statement_complete = True

        """
    
        return self
                    

class ExecuteFunctionNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        from tusk.variable import get_type_
        token = self.token
        self.name = token.value
        
        func = token.interpreter.data["funcs"][token.value] # [[], interpreter]
        func_name= token.value
        func_interpreter = func[1]
        parased_params = []
        if len(func[0]) > 0: # length of params, function doesnt need params
            for param in func[0]: # looping params (func[0] is the param list)
                e = self.interpreter.next_token() # next token, the code afer this checks if it matches the required param
                node = (await ExpressionNode(e).create())
                if len(param.split(":")) > 1:
                    if (await get_type_(node.value)) == param.split(":")[0].upper():
                        parased_params.append([param.split(":")[1],node.value])
                    else:
                        raise Exception(f"Recieved type {(await get_type_(await ExpressionNode(e).create()))} instead of {param.split(':')[0]} in function {token.value} ") 
                else:
                            parased_params.append([param,node.value])
        for i in parased_params: func_interpreter.data["vars"][i[0]] = i[1]
        func_interpreter.data["funcs"] = self.interpreter.data["funcs"]
        self.value = await func_interpreter.compile()
        return self