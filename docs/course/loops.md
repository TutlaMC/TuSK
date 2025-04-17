# Loops

Loops are things that go around and come around, similarly a loop here will be repition.

## For loop

This is a basic loop which has 2 types

- Looping all items/characters in a list/string
  - `loop all (items|characters) in <expression>`
  - This will loop all the characters/items in <expression> which is a string or list
- Looping a number of times
  - `loop <expression> times`
  - It will loop the code <expression> (as a number) times

You want to access the current item on the loop?
- TuSK has a default iter called `loop-item`
- If you want to use your on variable for this you can use `as <variable name>` after declaring the loop for example: `loop 10 times as x` and x will be the loop iteration

## While Loop

```lua
while <condition> do
...
end
```

It will execute the code below it if the condition is true infinitly until the condition becomes false

### Read `scripts/loops.tusk` for examples