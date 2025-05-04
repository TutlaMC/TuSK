from tusk.node import Node
from tusk.token import Token


class ConditionNode(Node):
    def __init__(self,token:Token):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.token = token

        self.opposite = False

        if token.type == "LOGIC" and token.value=="not":
            self.opposite = True
            token = self.interpreter.next_token()
        
        self.token = token

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        tkn1 = await ExpressionNode(self.token).create()
        if self.token.interpreter.get_next_token().type == "LOGIC":
            operator = self.interpreter.next_token()
            tkn2 = await ExpressionNode(self.interpreter.next_token()).create()
            if operator.value == "and" or operator.value == "&":
                if tkn1.value == True and tkn2.value == True: self.value = True
                else: self.value = False  
            elif operator.value == "or" or operator.value == "|":
                if tkn1.value == True or tkn2.value == True: self.value = True
                else: self.value = False  
            elif operator.value == "contains":
                if tkn2.value in tkn1.value: self.value = True
                else: self.value = False
            elif operator.value == "in":
                if tkn1.value in tkn2.value: self.value = True
                else: self.value = False
           
            self.type="3en"
        else:
            self.value = tkn1.value
            self.type="1en"

        if self.opposite: 
            if self.value == True: self.value = False
            else: self.value = True

        return self