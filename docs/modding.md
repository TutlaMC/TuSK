# Modding TUSK

One thing that makes TUSK better than everything else out there is because TUSK is open source and always ready for change and something new. We want more people to contribute to this project so we can become the best Discord bot builder. **You will need some python knowledge beforehand.

## Creating Custom Effects

(Written as of V0.0.2, `reply` might exist in the future but this was how it was made)
Let's say you wanted to create an effect called `reply` (replies to a mesage). You would follow these steps:

1. Declare it in the `src.tusk.lexer`
2. Create a file, or write it in an existing file
3. Import the required libraries
4. Code the "Node"
5. Creating the trigger in `src.tusk.nodes.effect`

### 1. Declaring it in the lexer

The lexer tokenizes everything, there can only be one type for each token so make a unique name. An example is the Get expression, though its an expression its mostly used as a keyword in requests (HTTP). Since we are creating `reply` we must first check if its already declared. If it is already declared as an effect we'll have to just edit the already existing code. **Removing something that already exists aor adding it even though it already exists could screw things up**

To declare it just add it to the end of the EFFECTS list:

```python
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
    "create",
    "reply" ################## <- here
]
```

### 2. Creating the file

The file technically could be created anywhere but its good practice to keep it in the `src/tusk/nodes` directory. Even better if you kept it organised and kept it in tehh `/effects` directory under nodes (Discord related effects such as this one will be done in `src/tusk/nodes/discord/effects` not `src/tusk/nodes/effects`)

Just create the python file with any name, since for this example we're doing something message related we'll use the already existing `messages_.py` file

### 3. Import the required libraries

At the beggining of your program add

```python
from tusk.node import Node
from tusk.token import Token
```

And since we're making something Discord related we'll also need:

```python

from tusk.discord_classes import *
OR
from tusk.discord_classes import MessageClass

import discord
```

I will just import everything (`*`)

### 4. Coding the "Node"

A Node is basically a node in the *Abstract Syntax Tree*. Here we'll you other nodes to add more branches such as an `ExpressionNode`.

```python
import discord

from tusk.node import Node
from tusk.token import Token

from tusk.discord_classes import *

class ReplyNode(Node):
    def __init__(self, token: Token):
        self.interpreter = token.interpreter
        self.token = token
    
    async def create(self):
        from tusk.nodes.expressions import ExpressionNode

        text = (await ExpressionNode(self.interpreter.next_token()).create()).value
        self.interpreter.expect_token("KEYWORD:to")

        message = (await ExpressionNode(self.interpreter.next_token()).create()).value
        message:discord.Message = await to_discord_object(self.interpreter.bot, message, "message")
        
        self.value = await message.reply(text)
        self.value = MessageClass(self.value)

        return self
```

Lets go line by line from the start of the node class on whats going on.

Firstly we're creating an initialization we're the node, we'll toke the **current token** the interpreter is on, if you want to see how tokens look like try using `src/compile.py "yourfile_here.tusk" --tokens`. The interpreter will just be the token's reference interpreter

Next we'll create an async function (this is necessary, or it may break stuff up) and then import ExpressionNode.

**What is an ExpressionNode?**

An ExpressionNode is how [Expressions](https://github.com/TutlaMC/TuSK/blob/main/docs/course/expressions.md) work, they are also wrappers for effects, the `value` property will be the output. Let's say they have a string as the next token, we could just get the next token right? The problem here is that what if it is a variable? Or what if it was going to be merged with another string using the `+` operator? The expression node solves, this (and also mathematical expressions!). 

**Why import it inside the class?**

We're using a lazy import otherwise we might create a [circular import](https://builtin.com/articles/python-circular-import). 



Next we get the text using the ExpressionNode. The ExpressionNode is also a node so we parase the token and then use the asynchronous create function to execute it and then pull the value using `.value`.

After getting the text, we need to follow the primary law of TUSK, **english like syntax** so instead of making it like a boring terminal command, we'll add some life to it by using some basic english grammar. Here we'll use the `interpreter.expect_token()` to expect the token `to` of type `KEYWORD`. There are many methods to implement this or other usecases where you don't want the interpreter to go to the next token or you just want to check it then you could use the `self.interpreter.get_next_token()` it will get the token without having to move the cursor further. There's also `self.interpreter.next_token()` that will just return the next token.

Next we get the message, the message could be an integer (read message docs) or a `MessageClass` so we'll use an `ExpressionNode` and then convert it to a Discord Object (`discord.Message` here) and then we'll reply to the message with the text. 

**What is the difference between `discord.Message`, `MessageClass` and my normal message in TUSK?**

- Your Message: It could be `event_message` or just a number (id, that is converted to a message). This is what users write in TUSK
- MessageClass: Bridge between TUSK and the interpreter, it will make it useable for us and the users but Discord wont accept this, so we use `discord.Message` for the reasons below.
- `discord.Message`: It is the class `discord.py` gives us for messages and is used to communicate with Discord, think of it as the branch between the interpreter and Discord


Finally we'll set the effect value to be the MessageClass (so its usable by TUSK users), setting the value will let it be used inside expressions, so I always reccomend you do this unless its a effect like `wait` where theres no use in returning anything.

### 5. Creating the trigger

Go to `src.tusk.nodes.effect.py` and go to the create function and in the if statement and add an `elif` statement that adds your effect:

```python
elif self.token.value == "reply":
    from tusk.nodes.discord.effects.message_ import ReplyNode
    self.value = await ReplyNode(self.token).create() # self.value = is not necessary but recoomended
```
