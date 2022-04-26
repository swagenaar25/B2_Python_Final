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
__all__ = ["error_format",
           "error_string",
           "random_color",
           "resource_path",
           "uuid",
           "license_notice",
           "ansi_to_hex",
           "has_accepted_license",
           "external_path",
           "LicenseConfirmationPopup"]

from tkinter import Misc
import tkinter as tk
from colorama import Fore, Back
from tkinter.simpledialog import Dialog
import random
import os
import sys
import typing


LICENSE_VERSION = "1"  # Change this if license changes, will require user to re-accept license


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


def external_path(relative_path: str) -> str:
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), relative_path)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def uuid() -> str:
    """Generate simple unique id"""
    chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
    out = ""
    for _ in range(16):
        out += random.choice(chars)
    return out


def has_accepted_license() -> bool:
    """Check whether user has accepted our license"""
    with open(external_path(".license_accepted.txt")) as file:
        return file.read().split("\n")[0] == LICENSE_VERSION


def set_accepted_license():
    """Record that the user has accepted the latest license"""
    with open(external_path(".license_path.txt"), "w") as file:
        file.write(LICENSE_VERSION)


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


class LicenseConfirmationPopup(Dialog):
    def __init__(self, parent: Misc | None):
        self.scrollable_license_frame = None
        self.accepted = False
        super().__init__(parent, "Accept License?")

    def body(self, master) -> None:
        self.scrollable_license_frame = tk.Frame(master)
        pass

    def buttonbox(self):
        """add standard button box.

        override if you do not want the standard buttons
        """

        box = tk.Frame(self)

        w = tk.Button(box, text="Accept", width=10, command=self.accept, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        # self.bind("<Return>", self.accept)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def accept(self, event=None):
        print("accepted")
        self.accepted = True
        self.destroy()

    def cancel(self, event=None):
        print("canceled")
        self.destroy()
