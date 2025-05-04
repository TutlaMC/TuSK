from tusk.interpreter import Interpreter
import discord
TuskInterpreter = Interpreter()
TuskInterpreter.setup(text="print 1189449886752591943", bot=discord.Client)
TuskInterpreter.compile()