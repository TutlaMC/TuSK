#########################################################
from discord import app_commands
from discord.ext import commands
import discord

def owner_only():
    async def predicate(ctx: discord.Interaction) -> bool:
        return ctx.user.id in ctx.client.config["roles"]["owners"]
    return app_commands.check(predicate)

def admin_only():
    async def predicate(ctx: discord.Interaction) -> bool:
        return ctx.user.id in ctx.client.config["roles"]["admins"].copy().append(ctx.client.config["roles"]["owners"])
    return app_commands.check(predicate)

def developer_only():
    async def predicate(ctx: discord.Interaction) -> bool:
        return ctx.user.id in ctx.client.config["roles"]["developers"].copy().append(ctx.client.config["roles"]["admins"]).append(ctx.client.config["roles"]["owners"])
    return app_commands.check(predicate)