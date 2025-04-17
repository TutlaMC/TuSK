# If statements

```lua
if <condition> then
...
elseif <conditon> then
...
else
...
end
```

- The Statement checks if the <condition> (read condition) is true, if it is  it will then execute the code after then, if it is false then the Interpreter skips it and goes to `elseif`, `else` or `end`. 
- Else & Elseif are not necessary, they are fall backs to the if statement. If the if statement is false it will then skip and execute all the elseif statements ( there can be infinite elseif statements ) until one is right or it could reach an else if an elseif is not present and it will execute it. 
- `end` Closes the structure
