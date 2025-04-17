# Functions

Functions are a set of instructions that will be executed when called

```lua
function IDENTIFIER <parameters> that 
...
end
```

- `function IDENTIFIER` creates a function named `IDENTFIER`
- <paramaters> are not necessary but is used to give functions data before they run as a variable
  -  a parameter must be a token name (read Token)
- A Function by default returns `true`, if you want it to return back a value you can use a return statement:
  - `return <expression>`
  - If you use it outside a function it will end the script because a function creates a seperate `Interpreter` (read Tokens)
  
Example:
```lua
function addnumbers num1 num2 that
    return num1 + num2
end

print addnumbers 3 2
```
*The reason I haven't named the function `add` in this example is because it is a builtin function for adding items to a list (Read Expression)*