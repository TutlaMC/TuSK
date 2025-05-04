from tusk.node import Node
from tusk.token import Token

class OnNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusk.interpreter import Interpreter
        event_type = self.interpreter.next_token()
        if event_type.type in ["EVENT_TYPE","KEYWORD"]:
            if event_type.type == "KEYWORD":
                if not event_type.value in ["message","reaction","voice","join","leave","typing"]:
                    self.interpreter.error("InvalidEvent", f"Invalid event type: {event_type.type}")





            self.end_found = False

            self.tokens = []
            interal_stucture_count = 0

            while self.end_found != True:
                nxt_tkn = self.interpreter.get_next_token()
                if nxt_tkn.type == "STRUCTURE":
                    interal_stucture_count += 1
                    tkn_to_append = self.interpreter.next_token()
                    self.tokens.append(tkn_to_append)
                elif nxt_tkn.type == "ENDSTRUCTURE":
                    if interal_stucture_count == 0:
                        self.interpreter.next_token()
                        self.end_found = True
                    else:
                        tkn_to_append = self.interpreter.next_token()
                        self.tokens.append(tkn_to_append)
                        interal_stucture_count -= 1
                else:
                    tkn_to_append = self.interpreter.next_token()
                    self.tokens.append(tkn_to_append)
            self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))

            self.interpreter.data["events"][event_type.value].append([self.tokens,self.interpreter])
        else:
            self.interpreter.error("InvalidEvent", f"Invalid event type: {event_type.type}")
        
        

