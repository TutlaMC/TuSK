import dbutil


from tusk.token import Token
from tusk.node import Node
from tusk.discord_classes import quick_convert_dsc, is_discord_object, is_tusk_object

class DBNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter

    async def create(self):
        from tusk.nodes.expressions import ExpressionNode
        if self.interpreter.get_next_token().value == "for":
            self.interpreter.next_token()
        id = (await ExpressionNode(self.interpreter.next_token()).create()).value

        if is_discord_object(id) or is_tusk_object(id):
            id = quick_convert_dsc(id)

        if id == None:
            self.interpreter.error("InvalidDatabaseID", f"Invalid database ID: {id}", notes=["Possible Fix: Make sure the ID is a valid integer/name/discord object"])

        if type(id) in [str,int]:
            id = str(id)
        else:
            id = str(id.id)

        if self.token.value == "setDBData":
            name = (await ExpressionNode(self.interpreter.next_token()).create()).value
            val = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.value = dbutil.set_data(id,name,val)
        elif self.token.value == "getDBData":
            name = (await ExpressionNode(self.interpreter.next_token()).create()).value
            val = dbutil.get_data(id,name)
            self.value = val
        elif self.token.value == "deleteDBData":
            name = (await ExpressionNode(self.interpreter.next_token()).create()).value
            self.value = dbutil.delete_data(id,name)
        elif self.token.value == "getDB":
            self.value = dbutil.get_db(id)
        elif self.token.value == "printDB":
            self.value = dbutil.get_db(id)
            print(self.value)
        elif self.token.value == "deleteDB":
            self.value = dbutil.delete_db(id)
        elif self.token.value == "createDB":
            self.value = dbutil.create_db(id)
        else:
            self.interpreter.error("InvalidDBOperation", f"Invalid database operation: {self.token.value}", notes=["Possible Fix: Make sure the operation is valid"])
        return self