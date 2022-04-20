__all__ = ["error_format", "error_string", "random_color"]

from colorama import Fore
import random


def error_format(msg: str) -> str:
    return Fore.RED + msg + Fore.RESET


def error_string(e: BaseException) -> str:
    out = ""
    try:
        out += e.__module__ + "."
    except AttributeError:
        pass
    out += e.__class__.__name__
    out += ": "
    out += e.__str__()
    return out


def random_color() -> str:
    vals = list("0123456789abcdef")
    out = "#"
    for _ in range(6):
        out += random.choice(vals)
    return out
