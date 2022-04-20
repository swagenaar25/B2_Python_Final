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


Author: Sam Wagenaar
Created: 4/13/2022
Modified: 4/20/2022
Purpose: Final Exam
Class: Intro to Programming
"""

import turtle
import tkinter as tk
from tkextrafont import Font
from queue import Queue
import os
from colorama import Fore, Back, Style
from command_lib import Command, CommandSet, InvalidCommandError
from callbacks import TurtleCallbacks
from standard_command_set import StandardCommandSet
import helpers

# window = turtle.Screen()
# window.title("Final Project Sam Wagenaar")

# bob = turtle.Turtle()
# bob.shape("classic")

kg = True


def quit_callback():
    global kg
    kg = False


#####################
# Register commands #
#####################
# standardCommandSet = StandardCommandSet(bob, window, quit_callback, print)

###########
# Run GUI #
###########

print("Type `help` for help")

'''
while kg:
    com = input(">> ")
    try:
        standardCommandSet.user_input(com)
    except InvalidCommandError as e:
        problem = "[LOOP] Something went wrong while executing that command:\n\t"
        problem += error_string(e)
        print(error_format(problem))'''


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Final Project Sam Wagenaar")
        self.canvas = tk.Canvas(master)
        self.canvas.config(width=600, height=600)
        self.canvas.pack(side=tk.LEFT)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("cyan")

        self.fonts = {"regular": Font(file="assets/fonts/FantasqueSansMono-Regular.ttf",
                                      family="Fantasque Sans Mono",
                                      size=13),
                      "bold": Font(file="assets/fonts/FantasqueSansMono-Bold.ttf",
                                   family="Fantasque Sans Mono",
                                   size=13,
                                   weight="bold"),
                      "italic": Font(file="assets/fonts/FantasqueSansMono-Italic.ttf",
                                     family="Fantasque Sans Mono",
                                     size=13,
                                     slant="italic"),
                      "bold_italic": Font(file="assets/fonts/FantasqueSansMono-BoldItalic.ttf",
                                          family="Fantasque Sans Mono",
                                          size=13,
                                          weight="bold",
                                          slant="italic")}

        self.console_frame = tk.Frame(self.master)
        self.console_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.console_out = tk.Text(self.console_frame,
                                   height=30,
                                   relief=tk.GROOVE,
                                   background="#2b2b2b",
                                   foreground="#ff00ff",
                                   font=self.get_font(),
                                   state=tk.DISABLED)
        self.console_out.pack(side=tk.TOP, fill=tk.BOTH)
        self.add_to_console(f"{Fore.RED}red text{Fore.GREEN}{Style.BRIGHT}Green bold text{Fore.RESET}Normal bold text{Back.MAGENTA}Magenta highlight bold text{Style.RESET_ALL}normal text")
        self.add_to_console(f"{Fore.LIGHTWHITE_EX}bright white text{Fore.BLUE}blue")
        self.add_to_console(f"Should be on newline normal")
        self.add_to_console(f"{Style.DIM}this is italic{Style.NORMAL} but this isn't")
        self.add_to_console(f"\thello")

        self.console_in = tk.Text(self.console_frame,
                                  height=1,
                                  relief=tk.GROOVE,
                                  background="#2b2b2b",
                                  foreground="#007F00",
                                  font=self.get_font(italic=True))
        self.console_in.pack(side=tk.TOP, fill=tk.X)

        self.my_lovely_turtle = turtle.RawTurtle(self.screen, shape="turtle")
        self.my_lovely_turtle.color("green")

    def clear_console(self):
        self.console_out.configure(state=tk.NORMAL)  # We need to be able to write
        self.console_out.delete("0.0", tk.END)
        self.console_out.configure(state=tk.DISABLED)  # User else needs to not write

    def _tag_from_params(self, fmt: str, fore_color: str, back_color: str) -> str:
        """Create a formatting tag from given parameters

        :param fmt: normal, bold, or italic
        :param fore_color: hex color
        :param back_color: hex color
        :return: tag id
        """
        name = helpers.uuid()
        self.console_out.tag_configure(name,
                                       foreground=fore_color,
                                       background=back_color,
                                       font=self.get_font(bold=(fmt == "bold"), italic=(fmt == "italic")))
        return name

    def add_to_console(self, string: str, end: str = "\n"):
        """Add text to console

        Implements certain ANSI codes:

        colorama.Fore.*

        colorama.Back.*

        colorama.Style.* (Dim is handled as italic)

        NOTE: Style is fully reset at end of text, \r doesn't work


        :param string: Text to add
        :param end: String to put at end of text
        :return: None
        """
        string += end
        # Build formatted segments
        segments = []  # segments of text, split by formatting changes (text, tag)
        segment = ""  # segment of text currently being built
        fmt = "normal"  # normal, bold, or italic
        fore_color = helpers.ansi_to_hex(Fore.WHITE)[1]
        back_color = None
        building_ansi = False  # If we are currently inside an ansi escape sequence
        building_text = True  # If we are currently inside of normal text
        ansi_start = "\x1b"
        safe_ansi_start = "\\x1b"
        ansi_end = "m"
        ansi_in_progress = ""
        for char in string:
            if char == ansi_start:  # Ansi start encountered
                print(segments)
                if building_text:  # We were building a segment of text, add it
                    segments.append((segment, self._tag_from_params(fmt, fore_color, back_color)))
                    segment = ""

                if building_ansi:
                    raise ValueError("Ansi start found while building ansi")

                building_ansi = True
                building_text = False
                ansi_in_progress = ansi_start
                print(f"Ansi start character found, bt: {building_text}, ba: {building_ansi}")
            elif building_ansi:  # We are in the middle of an ansi escape sequence
                print(f"fAnsi in progress: {ansi_in_progress.replace(ansi_start, safe_ansi_start)}")
                ansi_in_progress += char
                if char == ansi_end:  # Ansi sequence complete
                    if ansi_in_progress == Style.NORMAL:
                        fmt = "normal"
                    elif ansi_in_progress == Style.BRIGHT:
                        fmt = "bold"
                    elif ansi_in_progress == Style.DIM:
                        fmt = "italic"
                    elif ansi_in_progress == Style.RESET_ALL:
                        fmt = "normal"
                        fore_color = helpers.ansi_to_hex(Fore.WHITE)[1]
                        back_color = None
                    elif ansi_in_progress == Fore.RESET:
                        fore_color = helpers.ansi_to_hex(Fore.WHITE)[1]
                    elif ansi_in_progress == Back.RESET:
                        back_color = None
                    else:  # Maybe it is a color
                        try:
                            kind, color = helpers.ansi_to_hex(ansi_in_progress)
                            if kind == 0:
                                fore_color = color
                            elif kind == 1:
                                back_color = color
                            else:
                                raise ValueError("kind received other than 0 or 1")
                        except AttributeError:
                            print("Invalid ansi sequence received: "
                                  + ansi_in_progress.replace(ansi_start, safe_ansi_start))
                    ansi_in_progress = ""
                    building_ansi = False
            elif (not building_ansi) and (not building_text):  # We're not in an ansi sequence, and were in one before
                print("Reached end of escape sequence set")
                building_text = True
            if building_text:
                print(f"Adding char: {char}")
                segment += char
        # Make sure the last bit isn't ignored
        if building_text:  # We were building a segment of text, add it
            segments.append((segment, self._tag_from_params(fmt, fore_color, back_color)))
            segment = ""

        # Add formatted segments
        self.console_out.configure(state=tk.NORMAL)  # We need to be able to write
        for text, tag in segments:
            self.console_out.insert(tk.END, text, tag)
        self.console_out.configure(state=tk.DISABLED)  # User else needs to not write

    def do_stuff(self):
        for color in ["red", "yellow", "green"]:
            self.my_lovely_turtle.color(color)
            self.my_lovely_turtle.right(120)

    def press(self):
        self.do_stuff()

    def get_font(self, bold: bool = False, italic: bool = False):
        if bold and italic:
            return self.fonts["bold_italic"]
        elif bold:
            return self.fonts["bold"]
        elif italic:
            return self.fonts["italic"]
        else:
            return self.fonts["regular"]


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
