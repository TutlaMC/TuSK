from lark import Lark, Transformer

grammar = """
start: statement+

?statement: assignment
    | expr
    | keyword

    
?expr: expr "+" term -> add
    | expr "-" term -> sub
    | term

?term: term "*" factor -> mul
    | term "/" factor -> div
    | term "^" factor -> pow
    | term "%" factor -> mod
    | factor

?factor: SIGNED_NUMBER -> number
    | IDENTIFIER -> variable
    | "(" expr ")"
    | STRING -> string
    
    

    
?keyword: "print" expr -> print_expr
    | "if" condition "then" statement+ ("elseif" condition "then" statement+)* ("else" statement+)? "end" -> if_expr
    | "while" condition "do" statement+ "end" -> while_expr
    
?assignment: "set" IDENTIFIER "to" expr -> assign_var
    

?condition: expr COMPARE_SYMBOL expr -> comparision

COMPARE_SYMBOL: "<" | ">" | "==" | "!=" | "<=" | ">="
STRING: /"[^"]*"/

%import common.SIGNED_NUMBER
%import common.WS
%import common.CNAME -> IDENTIFIER
%ignore WS
"""

# FIX: IF STATEMENTS

class TuskInterpreter(Transformer):
    def __init__(self):
        self.vars = {}

    def assign_var(self, args):
        var_name = args[0]
        value = args[1]
        self.vars[var_name] = value
        return f"{var_name} = {value}"
    
    def if_expr(self, args):
        i = 0
        while i < len(args) - 1:
            condition = args[i]
            block = args[i + 1]
            if condition:
                return block
            i += 2
        if len(args) % 2 == 1:  # took 3 hours to fucking fix this
            return args[-1]
                  
        
    def comparision(self, args): # This is not a condition, a comparision is a type of condition (i got confused while programming this in so if your editing this then don mess up)
        left, comp, right = args
        comp = str(comp)
        if comp == "<":
            return left < right
        elif comp == ">":
            return left > right
        elif comp == "==":
            return left == right
        elif comp == "!=":
            return left != right
        elif comp == "<=":
            return left <= right
        elif comp == ">=":
            return left >= right
    
    # Variables & Types

    def variable(self, args):
        var = str(args[0])
        if var in self.vars: return self.vars[var]
        else: raise Exception(f"Variable '{var}' not defined")

    def number(self, number):
        return float(number[0])
    def string(self, string):
        return str(string[0])[1:-1] 
    
    # Operations
    def add(self, args):
        return args[0] + args[1]
    def sub(self, args):
        return args[0] - args[1]
    def mul(self, args):    
        return args[0] * args[1]
    def div(self, args):
        return args[0] / args[1]
    def pow(self, args):
        return args[0] ** args[1]
    def mod(self, args):
        return args[0] % args[1]
    def assign(self, args):
        return f"{args[0]} = {args[1]}"
    def identifier(self, args):
        return str(args[0])
    
    # Keywords
    def print_expr(self, args):
        print(args[0])
        return args[0]


with open("test.tusk") as f:
    code = f.read()

parser = Lark(grammar, parser="lalr", transformer = TuskInterpreter())
print("============== OUTPUT ===============")
tree = parser.parse(code)
print("\n============== TREE ===============")
print(tree.pretty())

