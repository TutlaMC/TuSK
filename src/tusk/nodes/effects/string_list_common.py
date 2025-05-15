from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode, FactorNode
from tusk.variable import is_ordinal_number

class AddNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import types_
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        item = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:to")
        list_ = (await FactorNode(self.interpreter.next_token()).create()).value
        if type(list_) in [float, int, str]: 
            self.value = item+list_
        elif type(list_) == dict:
            e = list(item.items())
            list_[e[0][0]] = e[0][1]
            self.value = list_
        else:
            list_.append(item)
            self.value = list_
        return self

class RemoveNode(Node):
    def __init__(self, token: Token):
        from tusk.variable import is_ordinal_number
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        item = is_ordinal_number(self.interpreter.next_token())
        self.interpreter.expect_token("KEYWORD:item")
        if item:
            item-=1
            self.interpreter.expect_token("KEYWORD:from")
            list_ = (await FactorNode(self.interpreter.next_token()).create()).value
            if type(list_) == list: 
                list_.pop(item)
                self.value = list_
            elif type(list_) == dict:
                key = list(list_.keys())[item]
                self.value = list_.pop(key)
            else:
                raise Exception(f"remove requires <list> not {type(list_)}")
        else: 
            raise Exception(f"remove expected ordinal number not {self.interpreter.current_token.value}, cardinal numbers are 1st, 2nd, 3rd, 4th, 5th...")
        return self

class ReplaceNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        to_replace = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:with")
        with_replace = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("LOGIC:in")
        list_ = (await FactorNode(self.interpreter.next_token()).create()).value
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
        return self

class SplitNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        to_split = (await ExpressionNode(self.interpreter.next_token()).create()).value
        nxt_tkn = self.interpreter.next_token()
        from_ = 0
        till_ = len(to_split)
        if nxt_tkn.type == "KEYWORD":
            if nxt_tkn.value == "by": 
                self.value = to_split.split(self.interpreter.expect_token("STRING").value)
            elif nxt_tkn.value in ["from", "till"]:
                _value = (await ExpressionNode(self.interpreter.next_token()).create()).value
                if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "till":
                    self.interpreter.next_token()
                    from_ = _value
                    till_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
                else: 
                    from_ = _value
                self.value = to_split[int(from_):int(till_)]
            else:
                raise Exception(f"Expected token KEYWORD:by | KEYWORD:from | KEYWORD:to got {nxt_tkn.type}")
        return self

class LengthNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        self.interpreter.expect_token("KEYWORD:of")
        e = (await FactorNode(self.interpreter.next_token()).create()).value
        self.value = len(e)
        return self



class IndexNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        to_index = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("LOGIC:in")
        list_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
        if type(list_) == str:
            self.value = list_.index(to_index)
        elif type(list_) == list:
            self.value = list_.index(to_index)
        elif type(list_) == dict:
            self.value = list_.index(to_index)
        else:
            raise Exception(f"index requires <string> or <list> not {type(list_)}")
        return self
