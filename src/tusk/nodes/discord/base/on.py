from tusk.node import Node
from tusk.token import Token

from tusk.discord_classes import get_exec_names


class OnNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusk.interpreter import Interpreter
        event_type = self.interpreter.next_token()
        if event_type.type in ["EVENT_TYPE","KEYWORD","EFFECT"]:
            if event_type.value == "delete":
                event_type_ = "_delete"
                e = self.interpreter.next_token()
                if e.type == "KEYWORD" and e.value == "message":
                    event_type_ = "message"+event_type_
                elif e.type == "KEYWORD" and e.value == "channel":
                    event_type_ = "channel"+event_type_
                elif e.type == "KEYWORD" and e.value == "role":
                    event_type_ = "role"+event_type_
                elif e.type == "KEYWORD" and e.value == "emoji":
                    event_type_ = "emoji"+event_type_
                else:
                    self.interpreter.error("InvalidEvent", f"Invalid event type: {event_type.type}")
            elif event_type.value == "remove":
                self.interpreter.expect_token("KEYWORD:reaction")
                event_type_ = "reaction_remove"
            elif event_type.value == "edit":
                self.interpreter.expect_token("KEYWORD:message")
                event_type_ = "message_edit"
            elif event_type.value == "create":
                e = self.interpreter.next_token()
                if e.type == "KEYWORD" and e.value == "channel":
                    event_type_ = "channel_create"
                elif e.type == "KEYWORD" and e.value == "role":
                    event_type_ = "role_create"
                elif e.type == "KEYWORD" and e.value == "emoji":
                    event_type_ = "emoji_create"
                else:
                    self.interpreter.error("InvalidEvent", f"Invalid event type: {event_type.type}")
            else: 
                event_type_ = event_type.value
                

            

            if not event_type_ in get_exec_names():

                self.interpreter.error("InvalidEvent", f"Invalid event type: {event_type_}")
            
            data = {}
            if self.interpreter.is_token("KEYWORD:toall"):
                self.interpreter.next_token()
                data["toall"] = True
            else:
                data["toall"] = False

            self.end_found = False

            self.tokens = []
            interal_stucture_count = 0

            while self.end_found != True:
                nxt_tkn = self.interpreter.get_next_token()
                if nxt_tkn.type == "STRUCTURE":
                    interal_stucture_count += 1
                    tkn_to_append = self.interpreter.next_token()
                    self.tokens.append(tkn_to_append)
                elif nxt_tkn.type in "ENDSTRUCTURE":
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
            data["tokens"] = self.tokens
            data["interpreter"] = self.interpreter
            self.interpreter.data["events"][event_type_].append(data)

            

        else:
            self.interpreter.error("InvalidEvent", f"Invalid event type: {event_type.type}")
        
        

