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
        self.commandSet.register(Command("forward", "Move forward ```distance``` pixels\n", 1, [int], self.call.forward))

        self.commandSet.register(Command("back", "Move back 50 pixels", 0, [], self.call.back, [50]))
        self.commandSet.register(Command("back", "Move back ```distance``` pixels\n", 1, [int], self.call.back))

        self.commandSet.register(Command("right", "Turn right 90 degrees", 0, [], self.call.right, [90]))
        self.commandSet.register(Command("right", "Turn right ```angle``` degrees\n", 1, [int], self.call.right))

        self.commandSet.register(Command("left", "Turn left 90 degrees", 0, [], self.call.left, [90]))
        self.commandSet.register(Command("left", "Turn left ```angle``` degrees\n", 1, [int], self.call.left))

        self.commandSet.register(Command("random", "Plot 20 random lines", 0, [], self.call.random, [20]))
        self.commandSet.register(Command("random", "Plot ```number``` random lines", 1, [int], self.call.random))

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
