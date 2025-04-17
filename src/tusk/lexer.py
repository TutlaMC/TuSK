from tusk.token import Token

KEYWORDS = [
      "to",
      "then", "elseif", "else",
      "that",
      "times","do","as",
      "what","type","convert",
      "characters","items","all",
      "input",
      "add","remove","split","replace","from","of","length","by","till"

]

EFFECTS = [
    "set",
    "print",
    "wait"
]

class Lexer:
    def __init__(self,text, interpreter):
        self.text = text

        self.pos = 0
        self.current_token = None

        self.tokens = []

        self.interpreter = interpreter
      

    
    def classify_tokens(self):
        stuff = self.text.split()

        text = self.text
        reader_pos = 0
        token = ""

        in_string = False
        in_comment = False
        start_quote_type = None     

        for i in "(){}[]+-/%*^,":
            text = text.replace(i,f" {i} ")
        text = text.replace("'s "," 's ")
        

        for j in text: 
            

            if in_string:
                if j == start_quote_type:
                    in_string = False
                    self.tokens.append(Token("STRING", token, self.interpreter))
                    token = ""
                else:
                    if start_quote_type=="'" and token=="s ":
                        in_string = False
                        self.tokens.append(Token("PROPERTY","'s ",self.interpreter))
                        token = ""
                    token += j
            elif in_comment:
                if j == "\n":
                    in_comment = False
                    token = ""
                else: pass
            else:
                
                if j in "(){}[],":
                    token_type = {
                        "(": "LEFT_PAR",
                        ")": "RIGHT_PAR",
                        "{": "LEFT_CURLY",
                        "}": "RIGHT_CURLY",
                        "[": "LEFT_SQUARE",
                        "]": "RIGHT_SQUARE",
                        ",": "COMMA",
                    }[j]
                    self.tokens.append(Token(token_type, j, self.interpreter))
                    token = ""
                elif j == "#":
                    in_comment = True
                    token = ""
                elif j in ["'", '"']:
                    in_string = True
                    start_quote_type = j
                    token = ""
                elif j in " \t\n" or reader_pos == len(text)-1:
                    if reader_pos == len(text)-1: token += j
                    """
                    if j in "\n":
                        self.tokens.append(Token("NEWLINE", j, self.interpreter))
                        token = ""
                    """
                    token = token.replace(" ","")
                    if token != "":
                        if token.isnumeric():
                            self.tokens.append(Token("NUMBER", token, self.interpreter))
                            token = ""
                        elif token in ["true","false"]:
                            self.tokens.append(Token("BOOL", token, self.interpreter))
                            
                            token = ""
                        elif token in ["and","or","not","contains","in","|","&"]:
                            self.tokens.append(Token("LOGIC", token, self.interpreter))
                            token = ""
                        elif token in ["<", ">", "<=", ">=", "==", "!=","is"]:
                            self.tokens.append(Token("COMPARISION", token, self.interpreter))
                            token = ""
                        elif token in KEYWORDS:
                            self.tokens.append(Token("KEYWORD", token, self.interpreter))
                            token = ""
                        elif token in EFFECTS:
                            self.tokens.append(Token("EFFECT",token,self.interpreter))
                            token=""
                        elif token in ["NUMBER","STRING","BOOL","BOOLEAN","LIST"]:
                            self.tokens.append(Token("TYPE",token, self.interpreter))
                            token=""
                        elif token in ["if","while","create","function","loop"]:
                            self.tokens.append(Token("STRUCTURE", token, self.interpreter))
                            token = ""
                        elif token in ["+", "-", "*", "/","**", "%"]:
                            self.tokens.append(Token("OPERATOR", token, self.interpreter))
                            token = ""
                        elif token == "end":
                            self.tokens.append(Token("ENDSTRUCTURE",token,self.interpreter))
                            token = ""
                        elif token in ["return"]:
                            self.tokens.append(Token("BREAKSTRUCTURE",token,self.interpreter))
                            token=""
                        else:
                            if not token in " \t\n": 

                                self.tokens.append(Token("IDENTIFIER", token, self.interpreter))
                                token = ""
                        
                        
                    

                    
                    
                    """
                    if j in "   ":
                        self.tokens.append(Token("TAB", token, self.interpreter))
                        token = ""                   
                    elif token == " ":
                        self.tokens.append(Token("WHITESPACE", token, self.interpreter))
                        token = ""
                    """
                else:
                    token += j

            reader_pos+= 1


                    
            '''
            elif token in " \t\n":
                self.tokens.append(Token("WHITESPACE", token))
            '''

        self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))

        ##  All this tab shi was done by chatgpt, it works so don't touch it
        """
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].type == "TAB":
                start = i
                count = 1
                while i + count < len(self.tokens) and self.tokens[i + count].type == "TAB":
                    count += 1

                tab_token = self.tokens[i]
                tab_groups = count // 4

                del self.tokens[start:start + count]

                for _ in range(tab_groups):
                    self.tokens.insert(start, Token("TAB", tab_token.value, self.interpreter))

                i = start + tab_groups
            else:
                i += 1
        i = 0
        while i < len(self.tokens) - 1:
            if self.tokens[i].type == "TAB" and self.tokens[i + 1].type == "NEWLINE":
                del self.tokens[i]
            else:
                i += 1


        # ight you can touch it now
        """


        # print(self.tokens, '<- tokens')
        return self.tokens