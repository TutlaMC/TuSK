from discord import app_commands
import discord
from discord.ext import commands
import discord
import requests

url = "https://raw.githubusercontent.com/TutlaMC/tusk/main/changelog.md"
response = requests.get(url)
changelog = response.text


class TuSKDefaultBotCore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="changelog",description="What's new?")
    async def changelog(self,interaction: discord.Interaction):
        await interaction.response.send_message(changelog)

    @app_commands.command(name="ping",description="Check the bot's latency")
    async def ping_callback(self,interaction: discord.Interaction):
        latency = interaction.client.latency * 1000  
        await interaction.response.send_message(f'Pong! Latency is {latency:.2f}ms')


    @app_commands.command(name="reload",description='Reload the bot data')
    async def reload_callback(self,interaction: discord.Interaction):
        self.bot.load_scripts()
        self.bot.reload_config()
        await interaction.response.send_message("Reloaded!",ephemeral=True)

    @app_commands.command(name="version",description='Check the bot version')
    async def version(self,interaction: discord.Interaction):
        await interaction.response.send_message(self.bot.config["version"])



async def setup(bot: commands.Bot):
    await bot.add_cog(TuSKDefaultBotCore(bot))