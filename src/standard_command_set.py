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
__all__ = ["StandardCommandSet"]

import turtle
from callbacks import TurtleCallbacks
from command_lib import CommandSet, Command
from helpers import error_format, error_string
import typing


class StandardCommandSet:
    def __init__(self,
                 pen: turtle.RawTurtle,
                 screen: turtle.TurtleScreen,
                 quit_callback: typing.Callable[[None], None],
                 output_callback: typing.Callable[[str], None]):
        """Create a standard set of commands for turtle interaction
        
        :param pen: Turtle to draw with
        :param screen: Screen to draw on
        :param quit_callback: Callback to quit program
        :param output_callback: Callback to send command output to
        """
        self.pen = pen
        self.screen = screen
        self.quit_callback = quit_callback
        self.output_callback = output_callback

        self.commandSet = CommandSet(self.output_callback)
        self.call = TurtleCallbacks(self.pen, self.screen, self.commandSet.output)

        self.commandSet.register(Command("penup", "Raise pen", 0, [], self.call.penup))
        self.commandSet.register(Command("pendown", "Lower pen\n", 0, [], self.call.pendown))

        self.commandSet.register(Command("forward", "Move forward 50 pixels", 0, [], self.call.forward, [50]))
        self.commandSet.register(
            Command("forward", "Move forward ```distance``` pixels\n", 1, [int], self.call.forward))

        self.commandSet.register(Command("back", "Move back 50 pixels", 0, [], self.call.back, [50]))
        self.commandSet.register(Command("back", "Move back ```distance``` pixels\n", 1, [int], self.call.back))

        self.commandSet.register(Command("right", "Turn right 90 degrees", 0, [], self.call.right, [90]))
        self.commandSet.register(Command("right", "Turn right ```angle``` degrees\n", 1, [int], self.call.right))

        self.commandSet.register(Command("left", "Turn left 90 degrees", 0, [], self.call.left, [90]))
        self.commandSet.register(Command("left", "Turn left ```angle``` degrees\n", 1, [int], self.call.left))

        self.commandSet.register(Command("random", "Plot 20 random lines", 0, [], self.call.random, [20]))
        self.commandSet.register(Command("random", "Plot ```number``` random lines", 1, [int], self.call.random))
        self.commandSet.register(Command(
            "tree_fractal",
            "Plot a tree fractal with starting branch length of 50, shortening of 5, and angle of 30",
            0,
            [],
            self.call.tree_fractal,
            [50, 5, 30]
        ))
        self.commandSet.register(Command(
            "tree_fractal",
            "Plot a tree fractal with starting branch length of ```branch_length```, shortening of ```shorten_by```, and angle of ```angle```",  # noqa
            3,
            [int, int, int],
            self.call.tree_fractal
        ))
        self.commandSet.register(Command(
            "koch_snowflake",
            "Plot a 3-sided koch snowflake fractal with a depth of 5",
            0,
            [],
            self.call.koch_snowflake,
            [3, 5]
        ))
        self.commandSet.register(Command(
            "koch_snowflake",
            "Plot a ```sides``` sided koch snowflake fractal with a depth of ```depth```",
            2,
            [int, float],
            self.call.koch_snowflake
        ))
        self.commandSet.register(Command(
            "koch_snowflake",
            "Plot a ```sides``` sided koch snowflake fractal with a depth of ```depth``` and scale of ```scale```",
            3,
            [int, float, float],
            self.call.koch_snowflake
        ))
        self.commandSet.alias("koch_snowflake", "snowflake")
        self.commandSet.alias("snowflake", "snow")

        self.commandSet.register(Command("color", "Set pen to ```color```", 1, [str], self.call.color))
        self.commandSet.register(Command("bgcolor", "Set background to ```color```", 1, [str], self.call.bgcolor))
        self.commandSet.alias("bgcolor", "bg")
        self.commandSet.register(Command("shape", "List pen shapes", 0, [], self.call.shapes))
        self.commandSet.register(Command("shape", "Set pen shape to ```shape```\n", 1, [str], self.call.shape))

        self.commandSet.register(Command("goto", "Move pen to (```x```, ```y```)\n", 2, [int, int], self.call.goto))

        self.commandSet.register(Command("pos", "Show pen's position", 0, [], self.call.pos))
        self.commandSet.register(Command("heading", "Show pen's heading", 0, [], self.call.heading))

        self.commandSet.register(Command("reset", "Reset everything\n", 0, [], self.call.reset))

        self.commandSet.register(Command("quit", "Close the canvas\n", 0, [], self.quit_callback))
        self.commandSet.alias("quit", "exit")

    def user_input(self, string: str):
        """Run command from user input

        :param string: User input
        :return: None
        """
        try:
            self.commandSet.execute(string)
        except Exception as e:  # noqa
            problem = f"Something went wrong while executing command [{string}]:\n\t"
            problem += error_string(e)
            self.output_callback(error_format(problem))
