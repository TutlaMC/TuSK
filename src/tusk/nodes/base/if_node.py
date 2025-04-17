from tusk.node import Node
from tusk.token import Token
from tusk.nodes.condition import *

class IfNode(Node):
    def __init__(self, token: Token):
        from tusk.interpreter import Interpreter
        from tusk.nodes.statement import StatementNode
        self.interpreter = token.interpreter

        condition = ConditionNode(token).value
        self.interpreter.expect_token("KEYWORD:then")
        self.statement = {
            "main": {"condition": condition, "code": None},
            "else": {"code": None},
        }


        self.end_found = False

        run_if = condition
        run_else = False

        
        
        while not self.end_found:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                self.end_found = True
            elif nxt_tkn.type=="KEYWORD" and nxt_tkn.value == "elseif":
                if run_if == False:
                    if ConditionNode(self.interpreter.next_token()).value:
                        self.interpreter.expect_token("KEYWORD:then")
                        run_if = True
                    else: run_if = False
            elif nxt_tkn.type=="KEYWORD" and nxt_tkn.value == "else":
                if run_if == False:
                    run_else = True
            else: 
                if run_if or run_else:
                    StatementNode(nxt_tkn)
                    
       

        
    """
        # If starts here
        self.if_interpreter = Interpreter()
        self.if_loop("main")

        self.statement_complete = False


        
        if condition:
            self.if_interpreter.setup(tokens=self.statement["main"]["code"], data=self.interpreter.data).compile()
            self.statement_complete = True
        else:
            for name in self.statement:
                if self.statement_complete:
                    break
                if type(name) == int:
                    if self.statement[name]["condition"]:
                        self.if_interpreter.setup(tokens=self.statement[name]["code"], data=self.interpreter.data).compile()
                        self.statement_complete = True
        if self.statement_complete != True:
            if self.statement["else"]["code"] != None:
                self.if_interpreter.setup(tokens=self.statement["else"]["code"], data=self.interpreter.data).compile()
                self.statement_complete = True

        self.value = self.statement_complete
        

    def if_loop(self, append_to_name):
        token_blocks = []
        interal_stucture_count = 0

        
        while self.end_found != True:
            nxt_tkn = self.interpreter.get_next_token()

            if nxt_tkn.type == "STRUCTURE":
                interal_stucture_count += 1
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter = self.if_interpreter
                token_blocks.append(tkn_to_append)
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "end":
                if interal_stucture_count == 0:
                    self.interpreter.next_token()
                    self.end_found = True
                else:
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter = self.if_interpreter
                    token_blocks.append(tkn_to_append)
                    interal_stucture_count -= 1
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "elseif":
                if interal_stucture_count == 0:  # ight then continue with elseif, otherwise the block might be continuing
                    self.interpreter.next_token()
                    condition = ExpressionNode(self.interpreter.next_token()).value
                    self.interpreter.expect_token("KEYWORD:then")

                    self.elseif_count += 1
                    self.statement[self.elseif_count] = {"condition": condition, "code": None}
                    self.if_loop(self.elseif_count)

                else:
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter = self.if_interpreter
                    token_blocks.append(tkn_to_append)
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "else":
                self.interpreter.next_token()
                self.if_loop("else")
            else:
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter = self.if_interpreter
                token_blocks.append(tkn_to_append)
        token_blocks.append(Token("ENDSCRIPT", "", self.interpreter))

        self.statement[append_to_name]["code"] = token_blocks
    """