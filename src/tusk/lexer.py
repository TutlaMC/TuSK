from tusk.token import Token
import discord

PermissionNames = {
    # Admin based
    "administrator": discord.Permissions.administrator,
    "ban_members": discord.Permissions.ban_members,
    "kick_members": discord.Permissions.kick_members,
    "deafen_members": discord.Permissions.deafen_members,
    "move_members": discord.Permissions.move_members,
    "mute_members": discord.Permissions.mute_members,
    "priority_speaker": discord.Permissions.priority_speaker,
    "manage_channels": discord.Permissions.manage_channels,
    "manage_emojis": discord.Permissions.manage_emojis,
    "manage_emojis_and_stickers": discord.Permissions.manage_emojis_and_stickers,
    "manage_events": discord.Permissions.manage_events,
    "manage_expressions": discord.Permissions.manage_expressions,
    "manage_guild": discord.Permissions.manage_guild,
    "manage_messages": discord.Permissions.manage_messages,
    "manage_nicknames": discord.Permissions.manage_nicknames,
    "manage_permissions": discord.Permissions.manage_permissions,
    "manage_roles": discord.Permissions.manage_roles,
    "manage_threads": discord.Permissions.manage_threads,
    "manage_webhooks": discord.Permissions.manage_webhooks,
    "moderate_members": discord.Permissions.moderate_members,
    "view_audit_log": discord.Permissions.view_audit_log,
    "view_guild_insights": discord.Permissions.view_guild_insights,
    "mention_everyone": discord.Permissions.mention_everyone,

    # Creation
    "create_expressions": discord.Permissions.create_expressions,
    "create_instant_invite": discord.Permissions.create_instant_invite,
    "create_private_threads": discord.Permissions.create_private_threads,
    "create_public_threads": discord.Permissions.create_public_threads,

    # Generic
    "read_message_history": discord.Permissions.read_message_history,
    "read_messages": discord.Permissions.read_messages,
    "send_messages": discord.Permissions.send_messages,
    "send_messages_in_threads": discord.Permissions.send_messages_in_threads,
    "send_tts_messages": discord.Permissions.send_tts_messages,
    "send_voice_messages": discord.Permissions.send_voice_messages,
    "embed_links": discord.Permissions.embed_links,
    "attach_files": discord.Permissions.attach_files,
    "change_nickname": discord.Permissions.change_nickname,
    "connect": discord.Permissions.connect,
    "add_reactions": discord.Permissions.add_reactions,
    "external_emojis": discord.Permissions.external_emojis,
    "external_stickers": discord.Permissions.external_stickers,
    "request_to_speak": discord.Permissions.request_to_speak,
    "speak": discord.Permissions.speak,
    "stream": discord.Permissions.stream,
    "use_application_commands": discord.Permissions.use_application_commands,
    "use_embedded_activities": discord.Permissions.use_embedded_activities,
    "use_external_emojis": discord.Permissions.use_external_emojis,
    "use_external_sounds": discord.Permissions.use_external_sounds,
    "use_external_stickers": discord.Permissions.use_external_stickers,
    "use_soundboard": discord.Permissions.use_soundboard,
    "use_voice_activation": discord.Permissions.use_voice_activation,
    "view_channel": discord.Permissions.view_channel,
}

KEYWORDS = [
      
      "then", "elseif", "else",
      "that",
      "times","do","as",
      "what","type",
      "characters","items","all",
      "from","of","by","till",
      "capture",
      "get","post","headers","json",
      "character","item","number",
      "file", "variable", 
      "channel", "server","member","user","message", "category", "emoji", "reaction", "role", "attachment",
      "channels", "servers", "members", "users", "messages", "categories", "emojis", "reactions", "roles", "attachments",
      "with","between",
      "named","color",
      "for", "can",
      "a", "an", "the","so","to",
      "toall",
      "can","cannot",
      "because",
      "delete_after"
      

]

EFFECTS = [
    "set",
    "print",
    "wait",
    "add","remove","split","replace", 
    "length",
    "input","convert",
    "shell", "python",
    "request",
    "index",
    "read","write","rename",
    "delete",
    "random",
    "import",
    
    # Discord
    "send","edit",
    "create",
    "allow","disallow",
    "change",
    "grant","revoke",
    "kick","ban","unban","timeout"
]

STRUCTURES = [
    "if","while","function","loop",
    "on"
]

EVENT_TYPES = [
    "voice","join","leave","typing", "ready"
    # read tusk.nodes.discord.base.on.py for more effects
]

COLORS = {
    "red":"#ff0000",
    "green":"#00ff00",
    "blue":"#0000ff",
    "yellow":"#ffff00",
    "purple":"#ff00ff",
    "orange":"#ffa500",
    "brown":"#a52a2a"
}

class Lexer:
    def __init__(self,text, interpreter):
        self.text = text

        self.pos = 0
        self.current_token = None

        self.tokens = []

        self.interpreter = interpreter
      
    def reg(self, name, value):
        self.tokens.append(Token(name.upper(), value, self.interpreter))
        self.ctoken = ""
    
    def classify_tokens(self):
        stuff = self.text.split()

        text = self.text
        reader_pos = 0
        self.ctoken = ""

        in_string = False
        in_comment = False
        hex_count = 0
        start_quote_type = None     

        for i in "(){}[],;:+-/%*^,":
            text = text.replace(i,f" {i} ")
        text = text.replace("'s "," 's ")
        

        for j in text: 
            if in_string:
                if j == start_quote_type:
                    in_string = False
                    self.ctoken = self.ctoken.replace("\\n","\n")
                    self.reg("STRING", self.ctoken)
                else:
                    if start_quote_type=="'" and self.ctoken=="s ":
                        in_string = False
                        self.tokens.append(Token("PROPERTY","'s ",self.interpreter))
                        self.ctoken = ""
                    self.ctoken += j
            elif in_comment:
                if j == "\n":
                    in_comment = False
                    self.ctoken = ""
                else: pass
            elif hex_count > 0:
                if j in "0123456789abcdef":
                    hex_count += 1
                    if hex_count == 7:
                        self.tokens.append(Token("COLOR", int("0x" + self.ctoken[1:] + j, 16), self.interpreter))
                        self.ctoken = ""
                        hex_count = 0
                    else:
                        self.ctoken += j
                else:
                    hex_count = 0
            else:
                if j in "(){}[],;:":
                    token_type = {
                        "(": "LEFT_PAR",
                        ")": "RIGHT_PAR",
                        "{": "LEFT_CURLY",
                        "}": "RIGHT_CURLY",
                        "[": "LEFT_SQUARE",
                        "]": "RIGHT_SQUARE",
                        ",": "COMMA",
                        ";": "SEMICOLON",
                        ":": "COLON",
                        "{": "LEFT_CURLY",
                        "}": "RIGHT_CURLY",
                    }[j]
                    self.tokens.append(Token(token_type, j, self.interpreter))
                    self.ctoken = ""
                elif j == "#":
                    if not (len(text) > reader_pos+6 and all(c.lower() in "0123456789abcdef" for c in text[reader_pos+1:reader_pos+7])):
                        in_comment = True
                        self.ctoken = ""
                    else:
                        hex_count = 1
                        self.ctoken = j
                        print(self.ctoken)
                elif j in ["'", '"']:
                    in_string = True
                    start_quote_type = j
                    self.ctoken = ""
                elif j in " \t\n" or reader_pos == len(text)-1:
                    if reader_pos == len(text)-1 and j not in " \t\n": 
                        self.ctoken += j
                    
                    self.ctoken = self.ctoken.replace(" ","").replace("\n","").replace("\t","")
                    if self.ctoken != "":
                        if self.ctoken.isnumeric():
                            self.tokens.append(Token("NUMBER", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["true","false"]:
                            self.tokens.append(Token("BOOL", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken == "nothing":
                            self.tokens.append(Token("NOTHING", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["and","or","not","contains","in","|","&"]:
                            self.tokens.append(Token("LOGIC", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["<", ">", "<=", ">=", "==", "!=","is"]:
                            self.tokens.append(Token("COMPARISION", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in KEYWORDS:
                            self.tokens.append(Token("KEYWORD", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in EFFECTS:
                            self.tokens.append(Token("EFFECT",self.ctoken,self.interpreter))
                            self.ctoken=""
                        elif self.ctoken in ["NUMBER","STRING","BOOL","BOOLEAN","LIST","NOTHING"]:
                            self.tokens.append(Token("TYPE",self.ctoken, self.interpreter))
                            self.ctoken=""
                        elif self.ctoken in STRUCTURES:
                            self.tokens.append(Token("STRUCTURE", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in EVENT_TYPES:
                            self.tokens.append(Token("EVENT_TYPE", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in PermissionNames:
                            self.reg("PERMISSION", self.ctoken)
                        elif self.ctoken in ["+", "-", "*", "/","**", "%"]:
                            self.tokens.append(Token("OPERATOR", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in COLORS or self.ctoken.startswith("#"):
                            if self.ctoken.startswith("#"):
                                if len(self.ctoken) != 7: self.interpreter.error("InvalidColor",f"{self.ctoken} is not a color (or valid hexcode)")
                                self.tokens.append(Token("COLOR", self.ctoken, self.interpreter))
                                self.ctoken = ""
                            else:
                                if self.ctoken not in COLORS: self.interpreter.error("InvalidColor",f"{self.ctoken} is not a color")
                                self.tokens.append(Token("COLOR", COLORS[self.ctoken], self.interpreter))
                                self.ctoken = ""
                        elif self.ctoken in ["miliseconds","seconds","minutes","hours","days","weeks","months","years","milisecond","second","minute","hour","day","week","month","year"]:
                            if self.ctoken.endswith("s"):
                                self.ctoken = self.ctoken[:-1]
                            self.tokens.append(Token("TIME", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken == "end":
                            self.tokens.append(Token("ENDSTRUCTURE",self.ctoken,self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["return","break"]:
                            self.tokens.append(Token("BREAKSTRUCTURE",self.ctoken,self.interpreter))
                            self.ctoken=""
                        else:
                            if not self.ctoken in " \t\n": 
                                self.tokens.append(Token("IDENTIFIER", self.ctoken, self.interpreter))
                                self.ctoken = ""
                else:
                    self.ctoken += j

            reader_pos += 1

        self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))
        return self.tokens