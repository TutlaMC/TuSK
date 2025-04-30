from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode

class AddNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import types_
        self.interpreter = token.interpreter
        
        item = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("KEYWORD:to")
        list_ = ExpressionNode(self.interpreter.next_token()).value
        if type(list_) in [float, int, str]: 
            self.value = item+list_
        elif type(list_) == dict:
            e = list(item.items())
            list_[e[0][0]] = e[0][1]
            self.value = list_
        else:
            list_.append(item)
            self.value = list_

class RemoveNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import is_ordinal_number
        self.interpreter = token.interpreter
        
        item = is_ordinal_number(self.interpreter.next_token())
        self.interpreter.expect_token("KEYWORD:item")
        if item:
            item-=1
            self.interpreter.expect_token("KEYWORD:from")
            list_ = ExpressionNode(self.interpreter.next_token()).value
            if type(list_) == list: 
                list_.pop(item)
                self.value = list_
            elif type(list_) == dict:
                key = list(list_.keys())[item]
                self.value = list_.pop(key)
                
            else:
                raise Exception(f"remove requires <list> not {type(list_)}")
                
        else: raise Exception(f"remove expected ordinal number not {self.interpreter.current_token.value}, cardinal numbers are 1st, 2nd, 3rd, 4th, 5th...")

class ReplaceNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        to_replace = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("KEYWORD:with")
        with_replace = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("LOGIC:in")
        list_ = ExpressionNode(self.interpreter.next_token()).value
        if type(list_) == str:
            self.value = str(list_).replace(to_replace,with_replace)
        elif type(list_) == list:
            e = []
            for i in list_:
                if i == to_replace: e.append(with_replace)
                else: e.append(i)
            self.value = e
        elif type(list_) == dict:
            list_[to_replace] = with_replace
            self.value = list_
        else:
            raise Exception(f"replace requires <string> or <list> not {type(list_)}")
        

class SplitNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        to_split = ExpressionNode(self.interpreter.next_token()).value
        nxt_tkn = self.interpreter.next_token()
        from_ = 0
        till_ = len(to_split)
        if nxt_tkn.type == "KEYWORD":
            if nxt_tkn.value == "by": self.value = to_split.split(self.interpreter.expect_token("STRING").value)
            elif nxt_tkn.value in ["from", "till"]:
                _value = ExpressionNode(self.interpreter.next_token()).value
                if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "till":
                    self.interpreter.next_token()
                    from_ = _value
                    till_ = ExpressionNode(self.interpreter.next_token()).value
                else: from_ = _value
                self.value = to_split[int(from_):int(till_)]
                        
            else:raise Exception(f"Expected token KEYWORD:by | KEYWORD:from | KEYWORD:to got {nxt_tkn.type}")

class LengthNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        self.interpreter.expect_token("KEYWORD:of")
        self.value = len(ExpressionNode(self.interpreter.next_token()).value)

class GetNode(Node): ### THIS IS A KEYWORD EVEN THOUGH ITS IN EFFECTS
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        self.interpreter.expect_token("KEYWORD:item|KEYWORD:character")
        self.interpreter.expect_token("KEYWORD:number")
        index = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("KEYWORD:of")
        list_ = ExpressionNode(self.interpreter.next_token()).value
        if type(list_) == str:
            self.value = list_[int(index)-1]
        elif type(list_) == list:
            self.value = list_[int(index)-1]

class IndexNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        
        to_index = ExpressionNode(self.interpreter.next_token()).value
        self.interpreter.expect_token("LOGIC:in")
        list_ = ExpressionNode(self.interpreter.next_token()).value
        if type(list_) == str:
            self.value = list_.index(to_index)
        elif type(list_) == list:
            self.value = list_.index(to_index)
        elif type(list_) == dict:
            self.value = list_.index(to_index)
        else:
            raise Exception(f"index requires <string> or <list> not {type(list_)}")
