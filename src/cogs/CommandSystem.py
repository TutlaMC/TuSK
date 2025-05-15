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
                        if len(param.split(":")) < 2:
                            param = "STRING:"+param
                        elif len(param.split(":")) == 2:
                            pass
                        else:
                            raise Exception(f"Invalid paramater for command '{command_name}': {param}")
                        params.append(param)
                    self.commands[command_name] = {
                            "name": command_name,
                            "file": os.path.join("scripts", filename),
                            "description": description,
                            "parameters": params
                        }
                    print(f"Loaded command: {command_name} - {description}")
        print(self.commands)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.cprint("Loading commands...",color="yellow")
        for command in self.commands:
            async def command_func(interaction: discord.Interaction):
                await self.execute_command(interaction, self.commands[command])
            command = app_commands.Command(
                name=self.commands[command]["name"],
                description=self.commands[command]["description"],
                callback=command_func
            )
            self.bot.tree.add_command(command)
        

        await self.bot.tree.sync()

    async def execute_command(self, interaction: discord.Interaction, command_name: str):
        if command_name not in self.commands:
            await interaction.response.send_message(f"Command {command_name} not found!", ephemeral=True)
            return

        await interaction.response.defer()

        try:
            interpreter = Interpreter()
            interpreter.setup(
                bot=self.bot,
                file=self.commands[command_name]["file"],
                is_cmd = True
            )

            interpreter.data["vars"]["event_channel"] = ChannelClass(interaction.channel)
            interpreter.data["vars"]["event_guild"] = GuildClass(interaction.guild)
            interpreter.data["vars"]["event_user"] = UserClass(interaction.user)
            result = await interpreter.compile()

            if result is not None:
                await interaction.followup.send(str(result))
            else:
                await interaction.followup.send("Command executed successfully!")
        except Exception as e:
            await interaction.followup.send(f"Error executing command: {str(e)}")

    @commands.command()
    @developer_only()
    async def reload_commands(self, ctx):
        logger.cprint("Reloading commands...",color="yellow")
        self.commands.clear()
        self.bot.tree.clear_commands()
        
        self.load_commands()
        
        for command_name, command_info in self.commands.items():
            async def command_func(interaction: discord.Interaction):
                await self.execute_command(interaction, command_name)
            
            command = app_commands.Command(
                name=command_name,
                description=command_info["description"],
                callback=command_func
            )
            self.bot.tree.add_command(command)
        
        await self.bot.tree.sync()
        await ctx.send("Commands reloaded successfully!")

async def setup(bot):
    await bot.add_cog(CommandSystem(bot)) 