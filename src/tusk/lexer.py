from tusk.token import Token

KEYWORDS = [
      "to",
      "then", "elseif", "else",
      "that",
      "times","do","as",
      "what","type",
      "characters","items","all",
      "from","of","length","by","till",
      "capture",
      "get","post","headers","json",
      "character","item","number",
      "file", "variable", 
      "channel", "server","member","user","message", "category", "emoji", "reaction",
      "channels", "servers", "members", "users", "messages", "categories", "emojis", "reactions",
      "with","between",
      "named","color"

]

EFFECTS = [
    "set",
    "print",
    "wait",
    "add","remove","split","replace", 
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
    "create"
]

STRUCTURES = [
    "if","while","create","function","loop",
    "on"
]

EVENT_TYPES = [
    "message","reaction","voice","join","leave","typing", "ready"
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
      
    def reg(self, name, val):
        self.tokens.append(Token("STRING", self.ctoken, self.interpreter))
        self.ctoken = ""
    
    def classify_tokens(self):
        stuff = self.text.split()

        text = self.text
        reader_pos = 0
        self.ctoken = ""

        in_string = False
        in_comment = False
        start_quote_type = None     

        for i in "(){}[],;:+-/%*^,":
            text = text.replace(i,f" {i} ")
        text = text.replace("'s "," 's ")
        

        for j in text: 
            if in_string:
                if j == start_quote_type:
                    in_string = False
                    self.ctoken = self.ctoken.replace("\\n","\n")
                    self.tokens.append(Token("STRING", self.ctoken, self.interpreter))
                    self.ctoken = ""
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