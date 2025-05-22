import os
from cog_core import *
import asyncio

from tusk.discord_classes import *
from tusk.interpreter import Interpreter
import logger

class CommandSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.load_commands()



    def load_commands(self):
        for filename in os.listdir("scripts"):
            if filename.endswith(".tuskcmd"):
                if not filename.startswith("--"):
                    with open(os.path.join("scripts", filename), "r") as f:
                        declaration = f.readline().strip()
                        if declaration.startswith("/"):
                            parts = declaration[1:].split(" ", 1)
                            command_name = parts[0]
                            
                            if len(parts) > 1:
                                rest = parts[1]
                                if rest.startswith('"'):
                                    desc_end = rest.find('"', 1)
                                    if desc_end != -1:
                                        description = rest[1:desc_end]
                                        parameters = rest[desc_end + 1:].strip()
                                    else:
                                        description = ""
                                        parameters = rest
                                else:
                                    description = ""
                                    parameters = rest
                            else:
                                description = ""
                                parameters = ""
                        else:
                            raise Exception(f"Invalid command: {filename}")

                        params = []
                        for param in parameters.split(" "):
                            if param:  # Skip empty parameters
                                if len(param.split(":")) < 2:
                                    param = "STRING:"+param
                                elif len(param.split(":")) == 2:
                                    pass
                                else:
                                    raise Exception(f"Invalid parameter for command '{command_name}': {param}")
                                params.append(param)
                        
                        self.commands[command_name] = {
                            "name": command_name,
                            "file": os.path.join("scripts", filename),
                            "description": description,
                            "parameters": params
                        }

    async def register_commands(self):
        self.load_commands()
        for command_name, command_info in self.commands.items(): # loops all command data
            async def make_command_func(cmd_info): # command parameter registration
                param_types = {
                    "STRING": str,
                    "INTEGER": int,
                    "BOOLEAN": bool,
                    "USER": discord.User,
                    "CHANNEL": discord.TextChannel,
                    "ROLE": discord.Role,
                    "MEMBER": discord.Member,
                    "ROLE": discord.Role
                }
                
                # Create the command function with parameters
                async def command_func(interaction: discord.Interaction):
                    await self.execute_command(interaction, cmd_info)                
                
                command = app_commands.Command(
                    name=cmd_info["name"],
                    description=cmd_info["description"],
                    callback=command_func,
                    
                )
                return command

            command_func = await make_command_func(command_info)
            self.bot.tree.add_command(command_func)
        print("Syncing")
        if len(self.commands.items()) > 0:
            await self.bot.tree.sync()
        print("Registered commands")
    async def execute_command(self, interaction: discord.Interaction, command_info: dict):
        await interaction.response.defer()

        try:
            interpreter = Interpreter()
            interpreter.setup(
                bot=self.bot,
                file=command_info["file"],
                is_cmd=True
            )

            interpreter.data["vars"]["ctx_channel"] = ChannelClass(interaction.channel)
            interpreter.data["vars"]["ctx_guild"] = GuildClass(interaction.guild)
            interpreter.data["vars"]["ctx_user"] = UserClass(interaction.user)
            interpreter.data["vars"]["ctx"] = ContextClass(interaction)
            for param in command_info["parameters"]:
                param_name = param.split(":")[0]
                if param_name in interaction.data.get("options", {}):
                    interpreter.data["vars"][param_name] = interaction.data["options"][param_name]["value"]
            await interpreter.compile()

        except Exception as e:
            await interaction.followup.send(f"Error executing command: {str(e)}")
            print(e.with_traceback())

    @commands.command()
    @owner_only()
    async def reload_commands(self, ctx):
        self.commands.clear()
        self.bot.tree.clear_commands()
        
        self.load_commands()
        await self.register_commands()
        
        await ctx.send("Commands reloaded successfully!")

async def setup(bot):
    cog = CommandSystem(bot)
    await cog.register_commands()
    await bot.add_cog(cog) 