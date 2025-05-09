# This file will let you test your code without intializing Discord

import discord
import sys
import asyncio
from tusk.interpreter import Interpreter
from tusk.discord_classes import get_exec_names
import json
file = sys.argv[1]

print(f"* NOTE THIS IS NOT THE SAME AS RUNNING THE BOT, THIS IS JUST FOR USING TUSK WITHOUT THE DISCORD FEATURES OR TESTING YOUR CODE BEFORE USING A BOT *\nCompiling file (BOT IS NOT INITIALIZED): {file}\n==========================================================\n")
interpreter = Interpreter()
class Client(discord.Client):
    def __init__(self):

        self.event_executors = get_exec_names()

        with open("config.json", "r") as f:
            self.config = json.load(f)
        self.startup_Flags = self.config["startup_flags"]

interpreter.setup(file=file,bot=Client())
if "--debug" in sys.argv:
    interpreter.debug = True
if "--tokens" in sys.argv:
    print(interpreter.tokens)


asyncio.run(interpreter.compile())
if "--data" in sys.argv:
    print(interpreter.data)
if "--vars" in sys.argv:
    print(interpreter.data["vars"])
if "--funcs" in sys.argv:
    print(interpreter.data["funcs"])
if "--events" in sys.argv:
    print(interpreter.data["events"],"\n")
if "--event-executors" in sys.argv:
    event_executors = get_exec_names()
    for event in interpreter.data["events"]:
        if interpreter.data["events"][event] != []:
            for exe in interpreter.data["events"][event].copy():
                event_executors[event].append(exe)
    print(event_executors)
if "--return" in sys.argv:
    print(interpreter.return_value)
print("==========================================================\n")
