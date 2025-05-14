from tusk.token import Token

def istusk(obj):
    if hasattr(obj,"value") and hasattr(obj,"properties"):
        return True
    return False

class Variable:
    def __init__(self,name, value, properties={}):
        self.name = name
        self.value = value
        self.properties = {}
        
    def update_property(self,property_name,property_value):
        self.value = self
        self.properties[property_name] = property_value

    def get_value(self):
        if istusk(self.value):
            return self.value.get_value()
        else:
            return self.value

    def __repr__(self):
        return f"<VARIABLE {self.name} = {self.value if self.value != self else ''}{self.properties}>"


types_ = {
    "NUMBER":float,
    "STRING":str,
    "BOOL": bool,
    "BOOLEAN":bool,
    "LIST": list,
    "TSON": dict,
    "NOTHING": None,
}
async def get_type_(token):
    
    from tusk.nodes.expressions import ExpressionNode
    
    if type(token) == Token: 
        e = await ExpressionNode(token).create()
        type_ = type(e.value)
    else: type_ = type(token)
    if type_ == float or type_ == int : return "NUMBER"
    elif type_ == str: return "STRING"
    elif type_ == bool: return "BOOL"
    elif type_ == list: return "LIST"
    elif type_ == dict: return "TSON"
    elif type_ == None: return "NOTHING"
    return f"<Pythonic:{str(type_)}>"

def is_ordinal_number(token: Token):
    if token.type == "IDENTIFIER":
        value = token.value.lower()
        if value.endswith("st") or value.endswith("nd") or value.endswith("rd") or value.endswith("th"):
            try:
                return int(value[:-2])
            except ValueError:
                return False
    return False 


