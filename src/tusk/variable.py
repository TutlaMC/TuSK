from tusk.token import Token

class Variable:
    def __init__(self,name, value, properties={}):
        self.name = name
        self.value = value
        self.properties = {}
        
    def update_property(self,property_name,property_value):
        self.value = self
        self.properties[property_name] = property_value
    def __repr__(self):
        return f"<VARIABLE {self.name} = {self.value if self.value != self else ''}{self.properties}>"


types_ = {
    "NUMBER":float,
    "STRING":str,
    "BOOL": bool,
    "BOOLEAN":bool,
    "LIST": list,
}
def get_type_(token:Token):
    from tusk.nodes.expressions import ExpressionNode
    type_ = type(ExpressionNode(token).value)
    if type_ == float or type_ == int : return "NUMBER"
    elif type_ == str: return "STRING"
    elif type_ == bool: return "BOOL"
    elif type_ == list: return "LIST"
    return 

def is_ordinal_number(token: Token):
    if token.type == "IDENTIFIER":
        value = token.value.lower()
        if value.endswith("st") or value.endswith("nd") or value.endswith("rd") or value.endswith("th"):
            try:
                return int(value[:-2])
            except ValueError:
                return False
    return False 


