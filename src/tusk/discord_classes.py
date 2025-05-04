from tusk.variable import Variable
import discord

class MessageClass(Variable):
    def __init__(self, message:discord.Message):

        self.name = message
        self.value = message.content
        self.properties = {}
        self.properties["content"] = message.content
        self.properties["author"] = message.author
        self.properties["channel"] = ChannelClass(message.channel)
        self.properties["channel_id"] = message.channel.id
        self.properties["guild"] = message.guild
        self.properties["created_at"] = str(message.created_at)
        self.properties["id"] = message.id
        self.properties["embeds"] = message.embeds
        self.properties["attachments"] = message.attachments
        self.properties["reactions"] = message.reactions
        self.properties["reference"] = message.reference
        self.properties["mentions"] = message.mentions
        self.properties["tts"] = message.tts
        
class UserClass(Variable):
    def __init__(self, user:discord.User):
        self.name = user
        self.value = user.name
        self.properties = {}
        self.properties["name"] = user.name
        self.properties["id"] = user.id
        self.properties["avatar"] = user.avatar
        self.properties["discriminator"] = user.discriminator
        self.properties["bot"] = user.bot
        self.properties["created_at"] = str(user.created_at)
        self.properties["joined_at"] = str(user.joined_at)
        self.properties["color"] = user.color
        self.properties["banner"] = user.banner
        self.properties["mention"] = user.mention

class GuildClass(Variable):
    def __init__(self, guild:discord.Guild):
        self.name = guild
        self.value = guild.name
        self.properties = {}
        self.properties["name"] = guild.name
        self.properties["id"] = guild.id
        self.properties["icon"] = guild.icon
        self.properties["created_at"] = str(guild.created_at)
        self.properties["member_count"] = guild.member_count
        self.properties["owner"] = UserClass(guild.owner)
        self.properties["afk_channel"] = guild.afk_channel
        self.properties["afk_timeout"] = guild.afk_timeout
        self.properties["roles"] = guild.roles
        self.properties["emojis"] = guild.emojis
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

class ChannelClass(Variable):
    def __init__(self, channel:discord.abc.GuildChannel):
        self.name = channel
        self.value = channel.name
        self.properties = {}
        self.properties["name"] = channel.name
        self.properties["id"] = channel.id
        self.properties["type"] = channel.type
        self.properties["position"] = channel.position
        self.properties["category"] = channel.category
        self.properties["topic"] = channel.topic
        self.properties["nsfw"] = channel.nsfw
        self.properties["guild"] = GuildClass(channel.guild)
        self.properties["members"] = channel.members
        
        
        