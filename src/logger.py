import json

def cprint(*args,color="normal",engine="tusk"):
    colors={
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "normal": "\033[0m",
        "end": "\033[0m"
    }
    print(f"{colors[color]}[{engine.upper()}]: {' '.join([str(arg) for arg in args])}{colors['end']}")
def debug_print(*args,color="blue",engine="debug"):
    with open("config.json", "r") as f:
        config = json.load(f)

    if config["debug"]:
        cprint(*args,color=color,engine=engine)