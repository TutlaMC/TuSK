class Node:
    def __init__(self, type_, name, values, auto_eval=False):
        self.type = type_
        self.auto_eval = False
        
        if self.type == "3n":
            self.value1 = values[0]
            self.operator = values[1]
            self.value2 = values[2]

            self.left_node = self.value
            self.operator_node = self.operator
            self.right_node = self.value2
        elif self.type == "2n":
            self.value1 = values[0]
            self.value2 = values[1]

            self.left_node = self.value
            self.right_node = self.operator
        elif self.type == "1n":
            self.value = values[0]
            self.left_node = self.value
        else: raise Exception("Node type not found")

# i have no clue what this is so js ignore this class, everything would still work if u didnt use this Node as the base NODe
