
import os
import discord
import random 
from math import *

from discord import app_commands
from discord.ext import tasks,commands

from tusk.interpreter import *
from tusk.discord_classes import *

from logger import *

class Client(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(intents=intents,command_prefix='.')

        self.event_executors = {
            "message":[],
            "reaction":[],
            "voice":[],
            "join":[],
            "leave":[],
            "typing":[]
        }

        with open("config.json", "r") as f:
            self.config = json.load(f)
        self.startup_Flags = self.config["startup_flags"]

    async def setup_hook(self):

        for filename in os.listdir('src/cogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'cogs.{filename[:-3]}')
        
        await self.tree.sync()




    async def on_ready(self):
        self.load_scripts()
        await self.compile_all_scripts()

    def load_scripts(self, enabled=True):
        if enabled:
            cprint("Loading scripts")
            scripts = os.listdir("scripts")
            scripts = [script for script in scripts if script.endswith(".tusk")]
            self.scripts = [f"scripts/{script}" for script in scripts if not script.startswith("--")]
            debug_print(scripts,config=self.config)
            return self.scripts
        else:
            cprint("Loading disabled scripts")
            scripts = os.listdir("scripts")
            scripts = [script for script in scripts if script.endswith(".tusk")]
            scripts = [f"scripts/{script}" for script in scripts if script.startswith("--")]
            debug_print(scripts,config=self.config)
            return scripts
        
    async def compile_all_scripts(self):
        for script in self.scripts:
            cprint(f"Compiling script: {script}")
            await self.compile_script(script)
            cprint(f"Compiled script: {script}",color="green")
        cprint("Compiled all scripts",color="green")

    async def compile_script(self,script:str, temporary=False):
        TuskInterpreter = Interpreter()
        if not temporary:
            TuskInterpreter.setup(bot=self, file=script)
            await TuskInterpreter.compile()
            self.remove_script_associations(script)
            for event in TuskInterpreter.data["events"]:
                print(self.event_executors)
                if TuskInterpreter.data["events"][event] != []:
                    self.event_executors[event].append(TuskInterpreter.data["events"][event])
                print(self.event_executors)
            

    def remove_script_associations(self,script:str):
        for event in self.event_executors:
            for executor in self.event_executors[event].copy():
                if executor[1].file == script:
                    self.event_executors[event].remove(executor)

    async def on_message(self,message:discord.Message): 
        debug_print("Executing message event",config=self.config)
        if message.author.bot: return
        for executor in self.event_executors["message"]:
            if executor != []:
                executor = executor[0]            
                event_interpreter = Interpreter()
                data = executor[1].data
                data["vars"]["event_message"] = MessageClass(message)
                data["vars"]["event_user"] = UserClass(message.author)
                data["vars"]["event_channel"] = ChannelClass(message.channel)
                data["vars"]["event_guild"] = GuildClass(message.guild)
                event_interpreter.setup(data=data,tokens=executor[0],bot=self)
                await event_interpreter.compile()

        debug_print("Message event executed",config=self.config)
    async def on_message_delete(self,message):
        pass
    async def on_message_edit(self,before,after):
        pass

    def reload_config(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)

client = Client()

@tasks.loop(minutes=1)
async def change_status():
    status = random.choice(client.config["status"]["loop"])
    await client.change_presence(activity=discord.Activity(type=status["type"], name=status["message"]))

@tasks.loop(minutes=10)
async def reload_config():
    client.reload_config()
#print(token)
with open("token.txt", "r") as f:
    token = f.read()
client.run(token)