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
            if type(item) != dict:
                self.interpreter.error("TypeError",f"Add requires <dict> not {type(item)}",notes=[f"Tusk has a weird way of handling dicts, so if you want to add something to a dictionary/dict you need to pass a dict/ Like let say you wanted to create a new key called 'name' with value 'john', you'll have to pass:\n|->  add {'name':'john'} to YOUR_DICT_HERE. Remember to save your dict in a variable if you want to store it, that's also a common error many people make, dicts are immutable."])
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
        
        if self.interpreter.is_token("KEYWORD:item"):
            self.interpreter.next_token()
            if self.interpreter.is_token("KEYWORD:number"):
                self.interpreter.expect_token("KEYWORD:number")
                num = (await ExpressionNode(self.interpreter.next_token()).create()).value
            else:
                num = is_ordinal_number(self.interpreter.next_token())
            if type(num) in [int,float]:
                idx = num-1
                self.interpreter.expect_token("KEYWORD:from|LOGIC:in")
                list_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
                if type(list_) == list: 
                    list_.pop(idx)
                    self.value = list_
                elif type(list_) == dict:
                    key = list(list_.keys())[idx]
                    list_.pop(key)
                    self.value = list_
                else:
                    self.interpreter.error("TypeError",f"remove requires <list> not {type(list_)}")
            else:
                self.interpreter.error("TypeError", "Expected a number, got a", [f"{type(num)}"])
        else:
            item = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.interpreter.expect_token("KEYWORD:from|LOGIC:in")
            list_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
            if type(list_) == list:
                list_.remove(item)
                self.value = list_
            elif type(list_) == dict:
                list_.pop(item)
                self.value = list_
            else:
                self.interpreter.error("TypeError",f"remove requires <list> not {type(list_)}")


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
        nxt_tkn = self.interpreter.get_next_token()
        from_ = 0
        till_ = len(to_split)
        if nxt_tkn.type == "KEYWORD":
            self.interpreter.next_token()
            if nxt_tkn.value == "by": 
                self.value = to_split.split((await ExpressionNode(self.interpreter.next_token()).create()).value)
            elif nxt_tkn.value in ["from", "till"]:
                if nxt_tkn.value == "from":
                    from_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
                if nxt_tkn.value == "till":
                    till_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
                elif self.interpreter.is_token("KEYWORD:till"):
                    self.interpreter.next_token()
                    till_ = (await ExpressionNode(self.interpreter.next_token()).create()).value
                self.value = to_split[int(from_):int(till_)]
            else:
                self.interpreter.error("UnexpectedToken", f"Expected token KEYWORD:by | KEYWORD:from | KEYWORD:to got {nxt_tkn.type}")
        else:
            self.value = to_split.split()
        return self

class LengthNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
        
    async def create(self):
        self.interpreter.expect_token("KEYWORD:of")
        e = (await ExpressionNode(self.interpreter.next_token()).create()).value
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
            self.value = list_.index(to_index)+1
        elif type(list_) == list:
            self.value = list_.index(to_index)+1
        elif type(list_) == dict:
            list_ = list(list_.keys())
            self.value = list_.index(to_index)+1
        else:
            raise Exception(f"index requires <string> or <list> not {type(list_)}")
        return self
