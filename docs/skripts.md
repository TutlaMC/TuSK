# Skripting

**What are skripts?**
Skripts are scripts that let you make bots in Discord. Its written in TuSK, you can learn to write in TuSK [here](https://github.com/TutlaMC/TuSK/blob/main/docs/home.md).

**How to manage your scripts**
Before you create your first script, you'll first want to understand how to manage it. All scripts that will run will be in the `scripts` directory (the scripts directory will be where you installed it- `your_directory/tusk/scripts/`). \

Putting "--" before a script will ignore it (disable it), but you'll still have to remove its associated data with `/remove_associated_data`.You can enable it back again by removing the -- but you'll have to compile it again on your own with `/compile`. This process can be simplified with the Script Panel

## The Script Panel

The script panel lets you manage your scripts within Discord! All you have to do is set your bot up and run `/scripts` and get started!

In the menu you will be able to see, add/remove, enable/disable & compile scripts. All you have to do is click buttons!

## Executing Scripts without Discord

**Repeatedly initialzing your bot to test code will get you rate limited.** So it's best to test algorithmic code or code that doesn't use Discord function/effects seperately during development. 

TuSK comes with a feature just for this (or if you want to run TuSK as a language without the Discord Bot features), to use it just run `src/compile.py your_script.tusk`. It comes with some flags:

`--debug`: Enables debug mode, showing token parsing and execution steps
`--tokens`: Shows the tokens generated from lexical analysis
`--data`: Lists the compiled data (variables, events and functions)
`--vars`: Lists the generated variables
`--funcs`: Lists the generated functions
`--events`: Lists the generated events
`--event-executors`: Lists the generated event executors
`--return`: Shows the returned value


Example execution:

```bash
src/compile.py "scripts/test.tusk" --debug --funcs --vars
```







