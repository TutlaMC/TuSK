import time
import asyncio

from tusk.node import Node
from tusk.token import Token

from tusk.nodes.expressions import ExpressionNode
from tusk.nodes.del_ import DelNode
class EffectNode(Node):
    def __init__(self, token: Token):
        self.token = token
        self.interpreter = token.interpreter
    async def create(self):
        self.interpreter.debug_msg(self.token, "<- effect (node) token")
        
        if self.token.value == "print":
            e = await ExpressionNode(self.interpreter.next_token()).create()
            print(e.value)
        elif self.token.value == "set":
            from tusk.nodes.effects.set import SetNode
            await SetNode(self.token).create()
        elif self.token.value == "wait":
            if self.interpreter.get_next_token().value == "for":
                try:
                    time.sleep((await ExpressionNode(self.interpreter.next_token()).create()).value)
                except KeyboardInterrupt as e:
                    self.interpreter.error("KeyboardInterrupt", "User cancelled wait", [f"You pressed Ctrl+C"])
            else:
                await asyncio.sleep((await ExpressionNode(self.interpreter.next_token()).create()).value)
        elif self.token.value == "delete":
            await DelNode(self.token).create()
        elif self.token.value == "write":
            from tusk.nodes.effects.fs import WriteNode
            await WriteNode(self.token).create()
        elif self.token.value == "rename":
            from tusk.nodes.effects.fs import RenameNode
            await RenameNode(self.token).create()
                    
        elif self.token.value == "input":
            from tusk.nodes.effects.input_ import InputNode
            self.value = (await InputNode(self.token).create()).value
        elif self.token.value == "convert":
            from tusk.nodes.effects.types_ import ConvertNode
            self.value = (await ConvertNode(self.token).create()).value
        elif self.token.value == "add":
            from tusk.nodes.effects.string_list_common import AddNode
            self.value = (await AddNode(self.token).create()).value
        elif self.token.value == "remove":
            from tusk.nodes.effects.string_list_common import RemoveNode
            self.value = (await RemoveNode(self.token).create()).value
        elif self.token.value == "replace":
            from tusk.nodes.effects.string_list_common import ReplaceNode
            self.value = (await ReplaceNode(self.token).create()).value
        elif self.token.value == "length":
            from tusk.nodes.effects.string_list_common import LengthNode
            self.value = (await LengthNode(self.token).create()).value
        elif self.token.value == "split":
            from tusk.nodes.effects.string_list_common import SplitNode
            self.value = (await SplitNode(self.token).create()).value
        elif self.token.value == "index":
            from tusk.nodes.effects.string_list_common import IndexNode
            self.value = (await IndexNode(self.token).create()).value
        elif self.token.value == "shell":
            from tusk.nodes.effects.exec_ import ShellNode
            self.value = (await ShellNode(self.token).create()).value
        elif self.token.value == "python":
            from tusk.nodes.effects.exec_ import PythonNode
            self.value = (await PythonNode(self.token).create()).value
        elif self.token.value == "request":
            from tusk.nodes.effects.requests_ import RequestNode
            self.value = (await RequestNode(self.token).create()).value
        elif self.token.value == "read":
            from tusk.nodes.effects.fs import ReadNode
            self.value = (await ReadNode(self.token).create()).value
        elif self.token.value == "random":
            from tusk.nodes.effects.random_ import RandomNode
            self.value = (await RandomNode(self.token).create()).value

        elif self.token.value == "import":
            from tusk.nodes.base.import_ import ImportNode
            await ImportNode(self.token).create()
        elif self.token.value == "json":
            from tusk.nodes.effects.json_ import JsonNode
            self.value = (await JsonNode(self.token).create()).value
        elif self.token.value in ["getDBData","setDBData","deleteDBData","getDB","printDB","deleteDB","createDB"]:
            from tusk.nodes.effects.db import DBNode
            self.value = (await DBNode(self.token).create()).value




        ####################### DISCORD EFFECTS #######################
        elif self.token.value in ["send","edit","reply"]:
            from tusk.nodes.discord.effects.messages_ import MessageNode
            self.value = (await MessageNode(self.token).create()).value
        elif self.token.value == "create":
            from tusk.nodes.discord.effects.create import CreateNode
            self.value = (await CreateNode(self.token).create()).value
        elif self.token.value == "allow":
            from tusk.nodes.discord.effects.permissions_ import AllowNode
            self.value = (await AllowNode(self.token).create())
        elif self.token.value == "disallow":
            from tusk.nodes.discord.effects.permissions_ import AllowNode
            self.value = (await AllowNode(self.token).create())
        elif self.token.value == "change":
            from tusk.nodes.discord.effects.change import ChangeNode
            self.value = (await ChangeNode(self.token).create())
        elif self.token.value == "grant":
            from tusk.nodes.discord.effects.roles import RoleNode
            self.value = (await RoleNode(self.token).create())
        elif self.token.value == "revoke":
            from tusk.nodes.discord.effects.roles import RoleNode
            self.value = (await RoleNode(self.token).create())
        elif self.token.value == "timeout":
            from tusk.nodes.discord.effects.admin import TimeoutNode
            self.value = (await TimeoutNode(self.token).create())
        elif self.token.value == "kick":
            from tusk.nodes.discord.effects.admin import KickNode
            self.value = (await KickNode(self.token).create())
        elif self.token.value == "ban":
            from tusk.nodes.discord.effects.admin import BanNode
            self.value = (await BanNode(self.token).create())
        elif self.token.value == "unban":
            from tusk.nodes.discord.effects.admin import UnbanNode
            self.value = (await UnbanNode(self.token).create())
            
        # delete is in tusk.nodes.del_

        return self