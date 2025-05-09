# V0.0.2-NT

**NT STANDS FOR NOT TESTED: THIS VERSION IS NOT TESTED SO YOU MAY RUN INTO ERRORS, REPORT THEM ON THE DISCORD**

ADDED:
- Importing (I want to see people build libraries out of this!) `import "file_name_here"`
- Non-Bot-Initalized Compiler (totest tusk code or run tusk seperate): `compile.py`
- Updated "modidng" in docs


NEW EFFECTS:
- `edit`
- `delete message|channel|category`
- `loop all channels|servers|categories|emojis|members/users in <server>|<channel>|<message>`
- `create channel|role`


NEW EVENTS:
- `delete message|channel|role|emoji`

- `create channel`

- `edit message`

- `reaction`
- `remove reaction`

- `join`
- `leave`




BACKEND:
- Reorganised effects by making it a single node instead of splitting the effect checks between the ExpressionNode and StatementNode
- Events are now given as dicts not lists