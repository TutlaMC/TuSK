# Token

Tokens are the building blocks of the language, they are declared in a [Lexer](https://stackoverflow.com/questions/11376089/what-is-the-purpose-of-a-lexer)

- The Lexer for this language is inefficient at the moment
- The lexer splits all operators in spaces so `**` wont work for powers
- The lexer ignores newlines unless its in a string or comment (in case of a comment it ends the comment there)
- The lexer automatically adds a token called `ENDSCRIPT` at the end of the script
- **Comments?** Yes we have comments! You can use a `#` and everything after that is ignored until a newline

We have different types of tokens:

- `STRING`: `"your text here"` or `'your text here'`
  - Beware: You cannot use `'s your text here'` because the lexer translates all `'s` to a `PROPERTY` token which is used for variable properties
- `BOOL`: `true`/`false`
- `NUMBER`: -inf to inf (inf are not numbers, just a representation of infinite)
- `COMPARISION`: `>=`, `<=`, `==`, `!=`, `is`
- `LOGIC`: `and`, `or`, `in`, `contains`, `&`, `|`
- `ENDSTRUCTURE`: `end`
- `BREAKSTRUCTURE`: `return`
- `KEYWORD`: Read `lexer.py`
- `EFFECT`: Read `lexer.py` 
- `LPAR`, `RPAR`, `LEFT_SQUARE`, `RIGHT_SQUARE`, `LEFT_CURLY`, `RIGHT_CURLY` which are (,),[,],{,} respectively

# Skripting (will be moved to another file)

Skripting is another word for programming in TuSK, right now all code you want to run should be done in `./scripts/test.tusk`

The Language first creates a [Lexer](https://stackoverflow.com/questions/11376089/what-is-the-purpose-of-a-lexer) (read Token) that tokenizes everything. Then it creates a [**Self Interpreter**](https://www.geeksforgeeks.org/introduction-to-interpreters/) which you can see how it works in `src/tusk/interpreter.py`.