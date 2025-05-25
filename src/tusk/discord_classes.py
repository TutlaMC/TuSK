from tusk.variable import Variable
import discord
import asyncio
from tusk.lexer import PermissionNames

def get_exec_names():
    return {
            "message":[], # triggered on message
            "message_edit":[], # triggered when message is edited

            "reaction":[], # triggered when reaction added
            "reaction_remove":[], # triggered when reaction removed

            "ready":[], # triggered when bot is ready
            "join":[], # triggered when member joins
            "leave":[], # triggered when member leaves
            "typing":[], # triggered when member is typing

            "channel_create":[], # triggered when channel is created
            "role_create":[], # triggered when role is created
            "emoji_create":[], # triggered when emoji is created

            "message_delete":[], # triggered when message is deleted
            "channel_delete":[], # triggered when channel is deleted
            "role_delete":[], # triggered when role is deleted
            "emoji_delete":[], # triggered when emoji is deleted
}

async def to_discord_object(bot, obj, to_type, references=[]):
    objl = []
    if not type(obj) == list:
        objl.append(obj)
    else:
        objl = obj
    dobjl = []
    for obj in objl:
        if type(obj) == Variable:
            tobj = obj.value
        elif to_type == "message":
            if type(obj) ==int:
                tobj = await bot.fetch_channel(references[0])
                tobj = await tobj.fetch_message(obj)
            elif type(obj) == MessageClass:
                tobj = obj.properties["python"]
            elif type(obj) == discord.Message:
                tobj = obj
        elif to_type == "channel":
            if type(obj) == int:
                tobj = await bot.fetch_channel(obj)
            elif type(obj) == ChannelClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.TextChannel, discord.abc.GuildChannel, discord.abc.PrivateChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel, discord.Thread]:
                tobj = obj
            elif type(obj) == ContextClass:
                tobj = obj.properties["python"]
            else:
                raise Exception(f"you fucked up lmao {obj}")
        elif to_type == "user":
            if type(obj) == int:
                tobj = await bot.fetch_user(obj)
            elif type(obj) == UserClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.Member, discord.User]:
                tobj = obj
        elif to_type == "guild":
            if type(obj) == int:
                tobj = await bot.fetch_guild(obj)
            elif type(obj) == GuildClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.Guild]:
                tobj = obj
        elif to_type == "role":
            if type(obj) == int:
                tobj = await bot.fetch_role(obj)
            elif type(obj) == RoleClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.Role]:
                tobj = obj
        elif to_type == "emoji":
            if type(obj) == int:
                tobj = await bot.fetch_emoji(obj)
            elif type(obj) == EmojiClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.Emoji]:
                tobj = obj
        elif to_type == "category":
            if type(obj) == int:
                tobj = await bot.fetch_channel(obj)
            elif type(obj) == CategoryClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.CategoryChannel]:
                tobj = obj
        elif to_type == "attachment":
            if type(obj) == int:
                tobj = await bot.fetch_channel(obj)
            elif type(obj) == AttachmentClass:
                tobj = obj.properties["python"]
            elif type(obj) in [discord.Attachment]:
                tobj = obj
        elif to_type == "context":
            if type(obj) == discord.Interaction:
                pass
            elif type(obj) == ContextClass:
                tobj = obj["python"]
        else:
            raise Exception(f"you fucked up lmao {obj}")
        dobjl.append(tobj)
    if len(objl) == 1:
        return dobjl[0]
    else:
        return dobjl


async def to_tusk_object(bot:discord.Client, obj, to_type, references=[]):
    objl = []
    if not type(obj) == list:
        objl.append(obj)
    else:
        objl = obj
    dobjl = []
    for obj in objl:
        dobj = None
        if to_type == "message":
            if type(obj) == discord.Message:
                dobj = MessageClass(obj)
            elif type(obj) == MessageClass:
                dobj = obj
            elif type(obj) == int:
                channel = await bot.fetch_channel(references[0])
                dobj = MessageClass(await channel.fetch_message(obj))
        elif to_type == "channel":
            if type(obj) == discord.TextChannel:
                dobj = ChannelClass(obj)
            elif type(obj) == ChannelClass:
                dobj = obj
            elif type(obj) == int:
                dobj = ChannelClass(await bot.fetch_channel(obj))
        elif to_type == "user":
            if type(obj) == discord.User:
                dobj = UserClass(obj)
            elif type(obj) == UserClass:
                dobj = obj
            elif type(obj) == int:
                dobj = UserClass(await bot.fetch_user(obj))
        elif to_type == "guild":
            if type(obj) == discord.Guild:
                dobj = GuildClass(obj)
            elif type(obj) == GuildClass:
                dobj = obj
            elif type(obj) == int:
                dobj = GuildClass(await bot.fetch_guild(obj))
        elif to_type == "role":
            if type(obj) == discord.Role:
                dobj = RoleClass(obj)
            elif type(obj) == RoleClass:
                dobj = obj
            elif type(obj) == int:
                chnl = await bot.fetch_channel(references[0])
                dobj = RoleClass(await chnl.fetch_role(obj))
        elif to_type == "emoji":
            if type(obj) == discord.Emoji:
                dobj = EmojiClass(obj)
            elif type(obj) == EmojiClass:
                dobj = obj
            elif type(obj) == int:
                chnl = await bot.fetch_guild(references[0])
                dobj = EmojiClass(await chnl.fetch_emoji(obj))
        elif to_type == "category":
            if type(obj) == discord.CategoryChannel:
                dobj = CategoryClass(obj)
            elif type(obj) == CategoryClass:
                dobj = obj
            elif type(obj) == int:
                guild = await bot.fetch_guild(references[0])
                dobj = CategoryClass(await guild.categories[obj])
        elif to_type == "attachment":
            if type(obj) == discord.Attachment:
                dobj = AttachmentClass(obj)
            elif type(obj) == AttachmentClass:
                dobj = obj
        else:
            raise Exception(f"you fucked up lmao {obj}")
        if dobj != None:
            dobjl.append(dobj)
    if len(objl) == 1:
        return dobjl[0]
    else:
        return dobjl

class MessageClass(Variable):
    def __init__(self, message:discord.Message|discord.PartialMessage):
        self.name = message
        self.value = message.content
        self.properties = {}
        self.properties["content"] = message.content
        self.properties["author"] = UserClass(message.author)
        self.properties["id"] = message.id
        if type(message) == discord.Message:
            self.properties["channel"] = ChannelClass(message.channel)
            self.properties["guild"] = GuildClass(message.guild)
            self.properties["server"] = self.properties["guild"]
            self.properties["created_at"] = str(message.created_at)
            self.properties["embeds"] = message.embeds
            self.properties["attachments"] = [AttachmentClass(attachment) for attachment in message.attachments]
            self.properties["has_attachments"] = len(self.properties["attachments"]) > 0
            self.properties["reactions"] = message.reactions
            if message.reference != None:
                if hasattr(message.reference, "message_id"):
                    self.properties["reference_id"] = message.reference.message_id
                else:
                    self.properties["reference_id"] = None
            else:
                self.properties["reference_id"] = None
            self.properties["mentions"] = message.mentions
            self.properties["tts"] = message.tts
            if hasattr(message, "guild"):
                self.properties["guild_id"] = message.guild.id
                self.properties["server_id"] = self.properties["guild_id"]
        self.properties["channel_id"] = message.channel.id
        
        
        self.properties["python"] = message
        
class UserClass(Variable):
    def __init__(self, user:discord.User|discord.Member):
        self.name = user
        self.value = user.name
        self.properties = {}
        self.properties["name"] = user.name
        self.properties["id"] = user.id
        self.properties["avatar"] = user.avatar
        self.properties["discriminator"] = user.discriminator
        self.properties["bot"] = user.bot
        self.properties["created_at"] = str(user.created_at)
        if hasattr(user, "joined_at"):
            self.properties["joined_at"] = str(user.joined_at)
        if hasattr(user, "status"):
            self.properties["online"] = user.status == discord.Status.online
        self.properties["color"] = user.color
        self.properties["banner"] = user.banner
        self.properties["mention"] = user.mention
        self.properties["usage"] = f"<@{self.properties['id']}>"
        if hasattr(user, "roles"): # this is a member
            self.properties["roles"] = [RoleClass(role) for role in user.roles]
            self.properties["top_role"] = RoleClass(user.top_role)
            self.properties["nick"] = user.nick
            self.properties["joined_at"] = str(user.joined_at)
            self.properties["member"] = True
        else: 
            self.properties["member"] = False
        self.properties["python"] = user

class GuildClass(Variable):
    def __init__(self, guild:discord.Guild, fast=False):
        self.name = guild
        self.value = guild.name
        self.properties = {}
        self.properties["name"] = guild.name
        self.properties["id"] = guild.id
        self.properties["icon"] = guild.icon
        self.properties["created_at"] = str(guild.created_at)
        self.properties["member_count"] = guild.member_count
        if guild.owner != None:
            self.properties["owner"] = UserClass(guild.owner)
        else:
            self.properties["owner"] = None
        self.properties["afk_channel"] = guild.afk_channel
        if fast == False:
            self.properties["roles"] = [RoleClass(role) for role in guild.roles]
            self.properties["emojis"] = [EmojiClass(emoji,list_parent=False) for emoji in guild.emojis]
        else:
            self.properties["roles"] = guild.roles
            self.properties["emojis"] = guild.emojis
            self.properties["afk_timeout"] = guild.afk_timeout
            self.properties["features"] = guild.features
            self.properties["premium_tier"] = guild.premium_tier
            self.properties["premium_subscription_count"] = guild.premium_subscription_count
            self.properties["system_channel"] = guild.system_channel
            self.properties["system_channel_flags"] = guild.system_channel_flags
            self.properties["widget_enabled"] = guild.widget_enabled
            self.properties["widget_channel"] = guild.widget_channel
            self.properties["widget_enabled"] = guild.widget_enabled
            self.properties["widget_channel"] = guild.widget_channel
            self.properties["voice_channels"] = guild.voice_channels
            self.properties["text_channels"] = guild.text_channels
            self.properties["categories"] = guild.categories
            self.properties["threads"] = guild.threads
        self.properties["python"] = guild
class ChannelClass(Variable):
    def __init__(self, channel,list_parent=True):
        self.name = channel
        self.value = channel.name
        self.properties = {}
        self.properties["name"] = channel.name
        self.properties["id"] = channel.id
        self.properties["type"] = channel.type
        if hasattr(channel, "position"):
            self.properties["position"] = channel.position
        else:
            self.properties["position"] = None
        self.properties["usage"] = f"<#{self.properties['id']}>"
        if type(channel) == discord.TextChannel:
            self.properties["topic"] = channel.topic
            self.properties["nsfw"] = channel.nsfw
        self.properties["guild"] = GuildClass(channel.guild)
        if list_parent:
            if channel.category != None:
                self.properties["category"] = CategoryClass(channel.category)
        self.properties["python"] = channel
        
class RoleClass(Variable):
    def __init__(self, role:discord.Role):
        self.name = role
        self.value = role.name
        self.properties = {}
        self.properties["name"] = role.name
        self.properties["id"] = role.id
        self.properties["color"] = role.color
        self.properties["position"] = role.position
        self.properties["permissions"] = role.permissions
        self.properties["mention"] = role.mention
        self.properties["members"] = None
        self.properties["usage"] = f"<@&{self.properties['id']}>"
        self.properties["python"] = role

class CategoryClass(Variable):
    def __init__(self, category:discord.CategoryChannel):
        self.name = category
        self.value = category.name
        self.properties = {}
        self.properties["name"] = category.name
        self.properties["id"] = category.id
        self.properties["position"] = category.position
        self.properties["mention"] = category.mention
        self.properties["channels"] = [ChannelClass(channel,list_parent=False) for channel in category.channels]
        self.properties["python"] = category

class EmojiClass(Variable):
    def __init__(self, emoji:discord.Emoji, is_str=False,other=None, list_parent=True):
        self.name = emoji
        self.value = emoji
        self.properties = {}
        if is_str:
            self.properties["name"] = emoji
            self.properties["id"] = emoji
            self.properties["is_animated"] = False
            self.properties["url"] = None
            self.properties["guild_id"] = other.guild.id
            if list_parent:
                self.properties["guild"] = GuildClass(other.guild)
                self.properties["server"] = self.properties["guild"]
            else:
                self.properties["guild"] = other.guild
                self.properties["server"] = other.guild
            
            self.properties["server_id"] = self.properties["guild_id"]
            self.properties["usage"] = emoji
        else:
            self.properties["name"] = emoji.name
            self.properties["id"] = emoji.id
            self.properties["is_animated"] = emoji.animated
            self.properties["url"] = emoji.url
            self.properties["guild_id"] = emoji.guild.id
            if list_parent:
                self.properties["guild"] = GuildClass(emoji.guild)
                self.properties["server"] = self.properties["guild"]
            else:
                self.properties["guild"] = emoji.guild
                self.properties["server"] = emoji.guild
            self.properties["server_id"] = self.properties["guild_id"]
            self.properties["usage"] = f"<:{self.properties['name']}:{self.properties['id']}>"
        self.properties["python"] = emoji

class ReactionClass(Variable):
    def __init__(self, reaction):
        self.name = reaction
        self.value = reaction.emoji
        self.properties = {}
        if type(reaction.emoji) == discord.Emoji:
            self.properties["emoji"] = EmojiClass(reaction.emoji)
        else:
            self.properties["emoji"] = EmojiClass(reaction.emoji, is_str=True, other=reaction.message.channel)
        self.properties["python"] = reaction

class AttachmentClass(Variable):
    def __init__(self, attachment:discord.Attachment|discord.File):
        self.name = attachment
        self.value = attachment.filename
        self.properties = {}
        self.properties["filename"] = attachment.filename
        if hasattr(attachment, "url"):
            self.properties["content"] = None
            self.properties["is_voice_message"] = attachment.is_voice_message()
            self.properties["spoiler"] = attachment.is_spoiler()
            self.properties["content_type"] = attachment.content_type
            self.properties["id"] = attachment.id
            self.properties["size"] = attachment.size
            self.properties["url"] = attachment.url
        else:
            self.properties["spoiler"] = False
        self.properties["python"] = attachment

class ContextClass(Variable):
    def __init__(self, context:discord.Interaction):
        self.name = context
        self.value = context
        self.properties = {}
        if hasattr(context, "message"):
            if context.message != None:
                self.properties["message"] = MessageClass(context.message)
        if hasattr(context, "channel"):
            if context.channel != None:
                self.properties["channel"] = ChannelClass(context.channel)
        if hasattr(context, "guild"):
            if context.guild != None:
                self.properties["guild"] = GuildClass(context.guild)
        if hasattr(context, "user"):
            if context.user != None:
                self.properties["user"] = UserClass(context.user)
        if hasattr(context, "guild_id"):
            if context.guild_id != None:
                self.properties["guild_id"] = context.guild_id
        self.properties["python"] = context

dsc_obj_types = [discord.Message,discord.TextChannel,discord.User,discord.Guild,discord.Role,discord.Emoji,discord.CategoryChannel,discord.Reaction,discord.Member, discord.PartialEmoji, discord.PartialMessage, discord.Attachment, discord.Interaction]
tusk_obj_types = [MessageClass,ChannelClass,UserClass,GuildClass,RoleClass,EmojiClass,CategoryClass,ReactionClass,AttachmentClass, ContextClass]



def is_discord_object(obj):
    if type(obj) in dsc_obj_types:
        return True
    return False

def is_tusk_object(obj):
    if type(obj) in tusk_obj_types:
        return True
    return False    

def quick_convert_dsc(obj):
    if is_tusk_object(obj):
        return obj.properties["python"]
    elif is_discord_object(obj):
        return obj
    else:
        return None
