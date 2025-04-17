# Expressions

Expressions are a bit complicated but once you understand them it will all be a piece of cake. There are 4 types of Expressions (its not exactly types, they form a tree going from root to shoot below) below:

- <factor>
- <term>
- <expression>
- <condition>

## Factor

This is the atom of TuSK. A Factor takes in a `NUMBER`, `STRING`, `BOOL`, `TYPE`, `KEYWORD` or `IDENTIFIER` token. A Factor could be:

- A Number
- A String
- A Boolean (true/false)
- A Type (any of the above)
- `( <expression> )` (So we can use brackets and combine <expression>s, this lets put <expression>s inside <expression>s aswell)
- A Function (aka `IDENTIFIER`)
- A Variable (aka `IDENTIFIER`)
  - Could be just a variable
  - Could be a property
  - Could be an item of a list/string, to access an item of a list/string you can `<ordinal number> item in <expression>` where ordinal number is 1st 2nd 3rd 4th 5th... and expression is a list/string
    - Example `3rd item in "javascript", "python", "kungfu"` returns `"kungfu"`
- A List 
  - Any expression seperated by commas will be made into a list
  - For example: `"bats", "balls", "wickets"` makes a list
- A Built in function
  - `replace`: `replace <expression> with <expression> in <expression>` 
    - Lets call all of these <expression>s: <expression> 1, 2 and 3 which are all strings
    - This function will replace whatever text is <expression>1, WITH <expression>2 to in <expression>3. 
    - For example `replace "bunnies" with "cats" in "i love bunnies"` will return "i love cats"
  - `what`: `what type is <expression>`
    - This just returns the `TYPE` for the <expression> (like a number or string)
    - For example: `what type is "hello"` returns string, `what type if false` returns boolean
  - `input`: `input <expression> `
    - <expression> must be a string
    - Takes in console input and returns whatever the user typed
    - Example `input "What's your age: "` and let's say the user typed "18" it will return 18
  - `add`: `add <expression> to <expression>`
    - expression1 is the item & expression2 must be a list
    - expression1 is added to expression2 
    - An Exception to this is when they are both numbers in which case it will just return the result
  - `remove`: `remove <expression> from <expression>`
    - Opposite to `add`
    - It will not subtract the expressions if they are numbers, it should be expression and list respectively
  - `convert`: `convert <expression> to TYPE`
    - Converts an expression to another type (read Token)
    - `TYPE` must be in uppercase
    - Let's say you ere adding two numbers but the values are strings, if you were to add them you would get a concatenation between them ("1" + "2" will return "12" as a string instead of 3 as an number). Convert lets you convert it to a number
    - For example: `convert 13 to STRING` will return "13"
  - `length`: `length of <expression>`
    - Returns how many items/characters are in an expression (expression must be list or string)
    - In case of list it will return the number of items and in string it will return number of characters
  - `split`: `split <expression> (by <expression>)|(from <expression> (till <expression>)? )`
    - Used for splitting lists/strings (string concatenation)
    - This is a bit complicated but in simple terms there are two modes:
      - Splitting by text
        - `split <expression> by <expression>`
        - Splits string (expression1) into a list for every time expression2 is repeated. 
        - Examples:
          - `split "Tutla Assistance is the greatest discord bot" by " "` returns ["Tutla","Assistance","is","the","greatest","discord,"bot"]
          - `split "Tutla Assistance is the greatest discord bot" by "greatest"` returns ["Tutla Assistance is the ", " discord bot"]
      - Splitting from range
        - `split <expression> from <expression> till <expression>`
        - Splits expression1 from (expression2 as a number) till (Expression3 as a number), these numbers are the characters
        - Tip: Try testing out this yourself!
  
## Term

A Term could be a <factor> or a `<factor> (/|*|^|%|) <factor>`:

- <factor> (Look at the previous heading, everything under there comes here even expressions because of parenthesis)
- <factor> * <factor>: Multiplication
- <factor> / <factor>: Division
- <factor> ^ <factor> or <factor> % <factor>
  
## Expression

Expressions are used everywhere in the language, they could be a:

- <term>
- <term> + <expression>
- <term> - <expression>
- <term> COMAPARISON <expression>
  - COMPARISION (Read token) could be is, <, >, <=, >=, ==, !=
  - returns a boolean (true/false)

## Condition

Conditions return true or false depending on what you give them

- `not` <condition>: returns the opposite of the condition, for example if it was true it will return false
- <expression> where it is a BOOL (true/false)
- <expression> LOGIC <expression>
  - LOGIC (read Token) can be and, or, contains, in
  - <expression> `and` or `&` <expression>: returns true if both are true
  - <expression> `|` or `or` <expression>: returns true if either are true
  - <expression> contains <expression>: returns true if expression2 is in expression1
  - <expression> in <expression>: returns true if expression1 is in expression2
  