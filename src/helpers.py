__all__ = ["error_format", "error_string", "random_color", "resource_path", "uuid", "license_notice", "ansi_to_hex"]
"""
Copyright (C) 2022  Sam Wagenaar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from colorama import Fore, Back
import random
import os
import sys
import typing


# input color: 007F00 italic
ansi_fore_to_hex = {
    Fore.BLACK: "#000000",
    Fore.BLUE: "#3993D4",
    Fore.LIGHTBLACK_EX: "#595959",
    Fore.LIGHTBLUE_EX: "#1FB0FF",
    Fore.LIGHTCYAN_EX: "#00E5E5",
    Fore.LIGHTGREEN_EX: "#4FC414",
    Fore.LIGHTMAGENTA_EX: "#ED7EED",
    Fore.LIGHTRED_EX: "#FF4050",
    Fore.LIGHTWHITE_EX: "#FFFFFF",
    Fore.LIGHTYELLOW_EX: "#E5BF00",
    Fore.CYAN: "#00A3A3",
    Fore.GREEN: "#5C962C",
    Fore.MAGENTA: "#A771BF",
    Fore.RED: "#F0524F",
    Fore.WHITE: "#808080",
    Fore.YELLOW: "#A68A0D"
}
ansi_back_to_hex = {
    Back.BLACK: "#000000",
    Back.BLUE: "#245980",
    Back.LIGHTBLACK_EX: "#424242",
    Back.LIGHTBLUE_EX: "#1778BD",
    Back.LIGHTCYAN_EX: "#006E6E",
    Back.LIGHTGREEN_EX: "#458500",
    Back.LIGHTMAGENTA_EX: "#B247B2",
    Back.LIGHTRED_EX: "#B82421",
    Back.LIGHTWHITE_EX: "#FFFFFF",
    Back.LIGHTYELLOW_EX: "#A87B00",
    Back.CYAN: "#154F4F",
    Back.GREEN: "#39511F",
    Back.MAGENTA: "#5C4069",
    Back.RED: "#772E2C",
    Back.WHITE: "#616161",
    Back.YELLOW: "#5C4F17"
}


def ansi_to_hex(ansi):
    try:
        return 0, ansi_fore_to_hex[ansi]
    except KeyError:
        try:
            return 1, ansi_back_to_hex[ansi]
        except KeyError:
            raise AttributeError("Invalid color")


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


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


def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    default = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    base_path = getattr(sys, '_MEIPASS', default)
    return os.path.join(base_path, relative_path)


def uuid() -> str:
    """Generate simple unique id"""
    chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
    out = ""
    for _ in range(16):
        out += random.choice(chars)
    return out


def license_notice() -> str:
    return """
Copyright (C) 2022  Sam Wagenaar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
