import json
import logging


def cprint(*args,color="normal",engine="tusk"):
    colors={
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "normal": "\033[0m",
        "end": "\033[0m"
    }
def debug_print(*args,config,color="blue",engine="debug"):
    if config["debug"]:
        logging.debug(f"[{engine.upper()}]: {' '.join([str(arg) for arg in args])}")

