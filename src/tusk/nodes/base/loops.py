from tusk.node import Node
from tusk.token import Token
from tusk.nodes.condition import *

class WhileNode(Node):
    def __init__(self, token: Token):
        from tusk.interpreter import Interpreter
        from tusk.nodes.statement import StatementNode
        self.token = token
        self.interpreter = token.interpreter
        self.cpos = self.interpreter.pos # position of condition start
        self.ecpos = self.cpos # position at ENDSTRUCTURE

        
        condition = ConditionNode(token).value
        self.interpreter.expect_token("KEYWORD:do")

        self.end_done = condition
        
        fned = False
        while fned != True:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                self.ecpos = self.interpreter.pos
                fned = True
            else: 
                self.interpreter.next_token()
        self.interpreter.pos = self.cpos
        ConditionNode(self.token)       
        

        
        
        while self.end_done:
            nxt_tkn = self.interpreter.next_token()
            if nxt_tkn.type=="ENDSTRUCTURE":
                self.check()
            else: 
                StatementNode(nxt_tkn)

             # recheck the condition
        self.interpreter.pos = self.ecpos
            

    def check(self):
        self.interpreter.pos = self.cpos
        condition = ConditionNode(self.token).value
        self.interpreter.expect_token("KEYWORD:do")
        self.end_done = condition
            
class LoopNode(Node):
    def __init__(self, token: Token):        
        self.token = token
        self.interpreter = token.interpreter
        

        self.as_ = None
        self.times = 0
        if token.type=="NUMBER":
            self.times = range(int(FactorNode(token).value))
            self.interpreter.expect_token("KEYWORD:times")
            e = self.set_as(token=self.interpreter.get_next_token())
            self.loop()
        elif token.type=="KEYWORD" and token.value == "all":
            loop_target_type = self.interpreter.expect_token("KEYWORD:items|KEYWORD:characters").value
            self.interpreter.expect_token("LOGIC:in")
            if loop_target_type == "characters":
                self.times = str(ExpressionNode(self.interpreter.next_token()).value)
                e = self.set_as(token=self.interpreter.get_next_token())
                self.loop()
            elif loop_target_type == "items":
                self.times = ExpressionNode(self.interpreter.next_token()).value
                e = self.set_as(token=self.interpreter.get_next_token())
                self.loop()
        
        else:
            raise Exception(f"loop expected token KEYWORD | NUMBER got {token.type}")

            
        


            
    def set_as(self, token:Token=None,value=None):
        if value != None:
            self.interpreter.data["vars"][self.as_] = value
        else:
            if token.type == "KEYWORD" and token.value == "as":
                self.interpreter.next_token()
                var = self.interpreter.next_token()
                if var.type == "IDENTIFIER":
                    self.as_ = var.value
                    self.interpreter.data["vars"][str(var.value)] = None
            else:
                self.as_ = "loop_item"
                self.interpreter.data["vars"][self.as_] = None
    def loop(self):
        from tusk.nodes.statement import StatementNode

        pos = self.interpreter.pos
        for i in self.times: 
            self.set_as(value=Variable(self.as_,i))

            end_block = False
            self.interpreter.pos = pos
            while end_block == False:
                nxt_tkn = self.interpreter.next_token()
                if nxt_tkn.type == "ENDSTRUCTURE":
                    end_block =True
                    break
                else:
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

        
        while self.end_done != True:
            nxt_tkn = self.interpreter.get_next_token()

            if nxt_tkn.type == "STRUCTURE":
                interal_stucture_count += 1
                tkn_to_append = self.interpreter.next_token()
                tkn_to_append.interpreter = self.if_interpreter
                token_blocks.append(tkn_to_append)
            elif nxt_tkn.type == "KEYWORD" and nxt_tkn.value == "end":
                if interal_stucture_count == 0:
                    self.interpreter.next_token()
                    self.end_done = True
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