#########################################################
from discord import app_commands
from discord.ext import commands
import discord

def owner_only():
    async def predicate(ctx: discord.Interaction) -> bool:
        return ctx.user.id in ctx.client.config["owners"]
    return app_commands.check(predicate)
