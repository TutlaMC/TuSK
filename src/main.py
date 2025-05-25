import os
import discord
import random 
import datetime
from math import *
import sys

from discord import app_commands
from discord.ext import tasks,commands

from tusk.interpreter import *
from tusk.discord_classes import *

from tusk.discord_classes import get_exec_names

from logger import *

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Client(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        with open("config.json", "r") as f:
            self.config = json.load(f)
        super().__init__(intents=intents,command_prefix=self.config["command_prefix"])
        self.event_executors = get_exec_names()

        
            
        
        # Start the tasks
        

    async def setup_hook(self):
        # Load cogs
        if self.config["preinstalled_commands"]:
            for filename in os.listdir('src/cogs'):
                if filename.endswith('.py'):
                    await self.load_extension(f'cogs.{filename[:-3]}')
            
            # Load packages
            if os.path.exists('packages'):
                for filename in os.listdir('packages'):
                    if filename.endswith('.py') and not filename.startswith('__'):
                        try:
                            await self.load_extension(f'packages.{filename[:-3]}')
                        except Exception as e:
                            print(f"Failed to load package {filename}: {e}")
            
            if self.config["jsk"]:
                cprint("Loading jishaku",color="green")
                try:
                    await self.load_extension("jishaku")
                    print("Successfully loaded Jishaku!")
                except Exception as e:
                    print(f"Failed to load Jishaku: {str(e)}")
                    print(f"Error type: {type(e)}")
                    import traceback
                    traceback.print_exc()

        await self.tree.sync()


    async def is_owner(self, user: discord.User):
        if user.id in self.config["owners"]:
            return True
        return await super().is_owner(user)
    
    async def on_ready(self):
        # Debug: Print loaded extensions
        print("\n=== Loaded Extensions ===")
        for ext in self.extensions:
            print(f"- {ext}")
        print("=======================\n")

        # Debug: Test Jishaku specifically
        if "jishaku" in self.extensions:
            print("Jishaku is loaded!")
            # Try to get Jishaku cog
            jsk = self.get_cog("Jishaku")
            if jsk:
                print("Jishaku cog found!")
                print(f"Available commands: {[c.name for c in jsk.get_commands()]}")
            else:
                print("Jishaku cog not found!")
        else:
            print("Jishaku is NOT loaded!")


        self.load_scripts()
        await self.compile_all_scripts()
        #status = random.choice(self.config["status"]["loop"])
        #await self.change_presence(activity=discord.Activity(type=status["type"], name=status["message"]))

        async def srd(data):
            return data
        await self.event_executor("ready",srd)
        await change_status.start()
        await reload_conf.start()

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

    async def compile_script(self,script:str, temporary=False,data:dict=None):
        TuskInterpreter = Interpreter()
        if not temporary:
            TuskInterpreter.setup(bot=self, file=script)
            self.remove_script_associations(script)
            await TuskInterpreter.compile()
            for event in TuskInterpreter.data["events"]:
                if TuskInterpreter.data["events"][event] != []:
                    for exe in TuskInterpreter.data["events"][event].copy():
                        self.event_executors[event].append(exe)

        else:
            TuskInterpreter.setup(bot=self, text=script)
            if "fake_channel" in data:
                if data["fake_channel"] != None:
                    TuskInterpreter.data["vars"]["event_channel"] = ChannelClass(data["fake_channel"])
            if "fake_user" in data:
                if data["fake_user"] != None:
                    TuskInterpreter.data["vars"]["event_user"] = UserClass(data["fake_user"],fast=True)
            await TuskInterpreter.compile()

            

    def remove_script_associations(self,script:str):
        for event in self.event_executors:
            for executor in self.event_executors[event].copy():
                if executor["interpreter"].file == script:
                    self.event_executors[event].remove(executor)

    def reload_config(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)

    async def event_executor(self,event:str,rd,other=None):
        for executor in self.event_executors[event]:
            if executor != []:
                event_interpreter = Interpreter()
                if not executor["toall"]:
                    if other.author.bot:
                        continue
                data = executor["interpreter"].data
                
                data = await rd(data)
                event_interpreter.setup(data=data,tokens=executor["tokens"],bot=self)
                await event_interpreter.compile()
    
    ########### EVENTS ###########
    async def on_message(self,message): 
        
        
        debug_print("Executing message event",config=self.config)
        if message.author.bot: return
        async def srd(data):
            data["vars"]["event_message"] = MessageClass(message)
            data["vars"]["event_user"] = UserClass(message.author)
            data["vars"]["event_channel"] = ChannelClass(message.channel)
            if hasattr(message, "guild"):
                data["vars"]["event_guild"] = GuildClass(message.guild,fast=True)
                data["vars"]["event_server"] = data["vars"]["event_guild"]
            return data
        await self.event_executor("message",srd,other=message)

        await self.process_commands(message)
        debug_print("Message event executed",config=self.config)
    async def on_message_delete(self,message):
        async def srd(data):
            data["vars"]["event_message"] = MessageClass(message)
            data["vars"]["event_user"] = UserClass(message.author)
            data["vars"]["event_channel"] = ChannelClass(message.channel)
            if hasattr(message, "guild"):
                data["vars"]["event_guild"] = GuildClass(message.guild,fast=True)
                data["vars"]["event_server"] = data["vars"]["event_guild"]
            return data
        await self.event_executor("message_delete",srd)
    async def on_message_edit(self,before,after):
        async def srd(data):
            data["vars"]["event_message"] = MessageClass(after)
            data["vars"]["event_message_old"] = MessageClass(before)
            data["vars"]["event_user"] = UserClass(after.author)
            data["vars"]["event_channel"] = ChannelClass(after.channel)
            if hasattr(after, "guild"):
                data["vars"]["event_guild"] = GuildClass(after.guild,fast=True)
                data["vars"]["event_server"] = data["vars"]["event_guild"]
            return data
        await self.event_executor("message_edit",srd)



    async def on_reaction_add(self,reaction,user):
        async def srd(data):
            data["vars"]["event_reaction"] = ReactionClass(reaction)
            data["vars"]["event_user"] = UserClass(user)
            data["vars"]["event_message"] = MessageClass(reaction.message)
            return data
        await self.event_executor("reaction",srd)

    async def on_reaction_remove(self,reaction,user):
        async def srd(data):
            data["vars"]["event_reaction"] = ReactionClass(reaction)
            data["vars"]["event_user"] = UserClass(user)
            data["vars"]["event_message"] = MessageClass(reaction.message)
            return data
        await self.event_executor("reaction_remove",srd)
    


    async def on_guild_channel_create(self,channel:discord.abc.GuildChannel):
        async def srd(data):
            data["vars"]["event_channel"] = ChannelClass(channel)
            data["vars"]["event_server"] = GuildClass(channel.guild,fast=True)
            return data
        await self.event_executor("channel_create",srd)
    
    async def on_guild_channel_delete(self,channel):
        async def srd(data):
            data["vars"]["event_channel"] = ChannelClass(channel)
            data["vars"]["event_server"] = GuildClass(channel.guild,fast=True)
            return data
        await self.event_executor("channel_delete",srd)

    async def on_guild_role_create(self,role:discord.Role):
        async def srd(data):
            data["vars"]["event_role"] = RoleClass(role)
            data["vars"]["event_server"] = GuildClass(role.guild,fast=True)
            return data
        await self.event_executor("role_create",srd)    

    async def on_guild_role_delete(self,role:discord.Role):
        async def srd(data):
            data["vars"]["event_role"] = RoleClass(role)
            data["vars"]["event_server"] = GuildClass(role.guild,fast=True)
            return data
        await self.event_executor("role_delete",srd)

    async def on_guild_emoji_create(self,emoji:discord.Emoji):
        async def srd(data):
            data["vars"]["event_emoji"] = EmojiClass(emoji)
            data["vars"]["event_server"] = GuildClass(emoji.guild,fast=True)
            return data
        await self.event_executor("emoji_create",srd)

    async def on_guild_emoji_delete(self,emoji:discord.Emoji):
        async def srd(data):
            data["vars"]["event_emoji"] = EmojiClass(emoji)
            data["vars"]["event_server"] = GuildClass(emoji.guild,fast=True)
            return data
        await self.event_executor("emoji_delete",srd)
        

    async def on_member_join(self,member:discord.Member):
        async def srd(data):
            data["vars"]["event_member"] = UserClass(member)
            data["vars"]["event_server"] = GuildClass(member.guild,fast=True)
            return data
        await self.event_executor("join",srd)

    async def on_member_remove(self,member:discord.Member):
        async def srd(data):
            data["vars"]["event_member"] = UserClass(member)
            data["vars"]["event_server"] = GuildClass(member.guild,fast=True)
            return data
        await self.event_executor("leave",srd)
    
    async def on_typing(self,channel:discord.abc.GuildChannel,user:discord.User,when:datetime.datetime):
        async def srd(data):
            data["vars"]["event_channel"] = ChannelClass(channel)
            data["vars"]["event_user"] = UserClass(user)
            return data
        await self.event_executor("typing",srd)
    """
    Coming in V0.0.3
    async def on_member_update(self,before,after):
        async def srd(data):
            data["vars"]["event_user"] = UserClass(after)
            data["vars"]["event_user_before"] = UserClass(before)
            data["vars"]["event_server"] = GuildClass(after.guild,fast=True)
            return data
        await self.event_executor("member_update",srd)

    """

    
    
@tasks.loop(minutes=1)
async def change_status():
    status = random.choice(client.config["status"]["loop"])
    if status["type"] == "online":
        status_type = discord.ActivityType.playing
    elif status["type"] == "idle":
        status_type = discord.ActivityType.idle
    elif status["type"] == "dnd":
        status_type = discord.ActivityType.dnd
    elif status["type"] == "offline":
        status_type = discord.ActivityType.listening
    elif status["type"] == "streaming":
        status_type = discord.ActivityType.streaming
    elif status["type"] == "playing":
        status_type = discord.ActivityType.playing
    elif status["type"] == "listening":
        status_type = discord.ActivityType.listening
    elif status["type"] == "watching":
        status_type = discord.ActivityType.watching
    await client.change_presence(activity=discord.Activity(type=status_type, name=status["message"]))


@tasks.loop(minutes=10)
async def reload_conf():
    client.reload_config()   

client = Client()



with open("token.txt", "r") as f:
    token = f.read()
client.run(token)