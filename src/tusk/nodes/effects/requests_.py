from tusk.token import Token
from tusk.node import Node
from tusk.nodes.expressions import ExpressionNode
from tusk.variable import Variable

import requests

class Reponse(Variable):
    def __init__(self,response:requests.Response):
        self.name = "reponse"
        
        self.properties = {
            "status_code": response.status_code,
            "headers": response.headers,
            "content": response.content,
            "text": response.text,
            "url": response.url,
        }
        try:
            self.properties["json"] = response.json()
        except Exception:
            print("NO JSON")

        self.value = response.text
        


class RequestNode(Node):
    def __init__(self, token: Token):
        self.interpreter= token.interpreter
        self.token = token
        
    async def create(self):
        self.interpreter.debug_msg(self.token)
        url = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.url = url.replace(" ","")
        data = {
            "headers": {},
            "data": {},
            "json": {},
            "files": {},
            "params": {},
            "cookies": {},
        }


        typ = self.interpreter.next_token()
        
        if typ.type == "KEYWORD" and typ.value == "get":
            if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "with":
                self.interpreter.next_token()
                while self.interpreter.get_next_token().value in data.keys():
                    name = self.interpreter.next_token().value.replace(" ","")
                    self.interpreter.expect_token("KEYWORD:as")
                    data[name] = (await ExpressionNode(self.interpreter.next_token()).create()).value
                    if self.interpreter.get_next_token().value == "and":
                        self.interpreter.next_token()
                    else:
                        break

            if "headers" in data:
                if "origin" in data["headers"]:
                    data["headers"]["origin"] = data["headers"]["origin"].replace(" ","")
                if "user-agent" in data["headers"]:
                    data["headers"]["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
            print(data, "get")
            self.value = Reponse(requests.get(self.url, params=data["params"], files=data["files"], cookies=data["cookies"], headers=data["headers"], json=data["json"]))

            
        elif typ.type == "KEYWORD" and typ.value == "post": 
            if self.interpreter.get_next_token().type == "KEYWORD" and self.interpreter.get_next_token().value == "with":
                self.interpreter.next_token()
                while self.interpreter.get_next_token().value in data.keys():
                    name = self.interpreter.next_token().value.replace(" ","")
                    self.interpreter.expect_token("KEYWORD:as")
                    data[name] = (await ExpressionNode(self.interpreter.next_token()).create()).value
                    if self.interpreter.get_next_token().value == "and":
                        self.interpreter.next_token()
                    else:
                        break

            if "headers" in data:   
                if "origin" in data["headers"]:
                    data["headers"]["origin"] = data["headers"]["origin"].replace(" ","")
                for i in data["headers"].copy().keys():
                    if "-" in i:
                        data["headers"][i.replace(" - ","-")] = data["headers"][i]
                        data["headers"].pop(i)
                if "user-agent" in data["headers"]:
                    data["headers"]["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
            print(data, "post")
            self.value = Reponse(requests.post(self.url,headers=data["headers"], json=data["json"]))
                    
        else: 
            raise Exception(f"Invalid request type: {typ.value}")

        self.returned_var = None
        return self
        
        