# This file will let you test your code without intializing Discord

import discord
import sys
import asyncio
from tusk.interpreter import Interpreter
from tusk.discord_classes import *
import json
file = sys.argv[1]

print(f"* NOTE THIS IS NOT THE SAME AS RUNNING THE BOT, THIS IS JUST FOR USING TUSK WITHOUT THE DISCORD FEATURES OR TESTING YOUR CODE BEFORE USING A BOT *\nCompiling file (BOT IS NOT INITIALIZED): {file}\n==========================================================\n")
interpreter = Interpreter()
class Client(discord.Client):
    def __init__(self):

        self.event_executors = get_exec_names()

        with open("config.json", "r") as f:
            self.config = json.load(f)
bot=Client()
interpreter.setup(file=file,bot=bot)
if "--debug" in sys.argv:
    interpreter.debug = True
if "--tokens" in sys.argv:
    print(interpreter.tokens)


asyncio.run(interpreter.compile())
event_executors = get_exec_names()
for event in interpreter.data["events"]:
    if interpreter.data["events"][event] != []:
        for exe in interpreter.data["events"][event].copy():
            event_executors[event].append(exe)
if "--data" in sys.argv:
    print(interpreter.data)
if "--vars" in sys.argv:
    print(interpreter.data["vars"])
if "--funcs" in sys.argv:
    print(interpreter.data["funcs"])
if "--events" in sys.argv:
    print(interpreter.data["events"],"\n")
if "--event-executors" in sys.argv:
    print(event_executors)
if "--return" in sys.argv:
    print(interpreter.return_value)

if "--exec-event" in sys.argv:
    event = sys.argv[sys.argv.index("--exec-event")+1]
    if event in event_executors:
        for exe in event_executors[event]:
            if exe != []:
                event_interpreter = Interpreter()
                data = exe["interpreter"].data
                ### Test data
                guild = discord.Guild
                channel = discord.TextChannel
                message = discord.Message
                reaction = discord.Reaction
                user = discord.User
                if event == "reaction":
                    data["vars"]["event_reaction"] = ReactionClass(reaction)
                    data["vars"]["event_user"] = UserClass(user)
                    print(data["vars"]["event_reaction"])
                elif event == "message":
                    data["vars"]["event_message"] = MessageClass(message)
                elif event == "message_delete":
                    data["vars"]["event_message"] = MessageClass(message)
                elif event == "message_edit":
                    data["vars"]["event_message"] = MessageClass(message)
                elif event == "reaction_remove":
                    data["vars"]["event_reaction"] = ReactionClass(reaction)
                    data["vars"]["event_user"] = UserClass(user)
                event_interpreter.setup(data=data,tokens=exe["tokens"],bot=bot)
                asyncio.run(event_interpreter.compile())
                print(event_interpreter.return_value)
print("==========================================================\n")
