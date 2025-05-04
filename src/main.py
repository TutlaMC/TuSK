
import os
import discord
from discord import app_commands
import random as ran
from discord.ext import tasks,commands
from math import *
import traceback
import asyncio

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

    async def setup_hook(self):
        """
        for filename in os.listdir('modules/Cogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'modules.Cogs.{filename[:-3]}')
        
        for filename in os.listdir('modules/AdvancedCogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'modules.AdvancedCogs.{filename[:-3]}')
        await client.load_extension(f'modules.CLIENT.help')
        await self.tree.sync()
        """






    async def on_ready(self):
        cprint("Loading scripts")
        scripts = os.listdir("scripts")
        

        scripts = [script for script in scripts if script.endswith(".tusk")]
        scripts = [f"scripts/{script}" for script in scripts if not script.startswith("--")]
        debug_print(scripts)
        for script in scripts:
            cprint(f"Loading script: {script}")
            TuskInterpreter = Interpreter()
            TuskInterpreter.setup(bot=self, file=script)
            await TuskInterpreter.compile()
            for event in TuskInterpreter.data["events"]:
                self.event_executors[event].append(TuskInterpreter.data["events"][event])

            cprint(f"Loaded script: {script}",color="green")
        cprint("Loaded all scripts",color="green")



    async def on_message(self,message:discord.Message): 
        debug_print("Executing message event")
        if message.author.bot: return
        for executor in self.event_executors["message"]:
            executor = executor[0]
            # executor[0] is the message event interpreter
            # executor[1] is the original interpreter
            
            event_interpreter = Interpreter()
            data = executor[1].data
            data["vars"]["event_message"] = MessageClass(message)
            data["vars"]["event_user"] = UserClass(message.author)
            data["vars"]["event_channel"] = ChannelClass(message.channel)
            data["vars"]["event_guild"] = GuildClass(message.guild)
            event_interpreter.setup(data=data,tokens=executor[0],bot=self)
            await event_interpreter.compile()
        debug_print("Message event executed")
    async def on_message_delete(self,message):
        pass
    async def on_message_edit(self,before,after):
        pass



client = Client()






token = os.getenv("TOKEN")
#print(token)
client.run("YOUR_TOKEN")