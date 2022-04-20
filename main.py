"""
Author: Sam Wagenaar
Created: 4/13/2022
Modified: 4/13/2022
Purpose: Final Exam
Class: Intro to Programming
"""

import turtle
from queue import Queue
from command_lib import Command, CommandSet, InvalidCommandError
from callbacks import TurtleCallbacks
from helpers import error, error_string

window = turtle.Screen()
window.title("Final Project Sam Wagenaar")

bob = turtle.Turtle()
bob.shape("classic")

kg = True


def quit_callback():
    global kg
    kg = False


#####################
# Register commands #
#####################
commandSet = CommandSet(print)

call = TurtleCallbacks(bob, window, commandSet.output)

commandSet.register(Command("penup", "Raise pen", 0, [], call.penup))
commandSet.register(Command("pendown", "Lower pen\n", 0, [], call.pendown))

commandSet.register(Command("forward", "Move forward 50 pixels", 0, [], call.forward, [50]))
commandSet.register(Command("forward", "Move forward ```distance``` pixels\n", 1, [int], call.forward))

commandSet.register(Command("back", "Move back 50 pixels", 0, [], call.back, [50]))
commandSet.register(Command("back", "Move back ```distance``` pixels\n", 1, [int], call.back))

commandSet.register(Command("right", "Turn right 90 degrees", 0, [], call.right, [90]))
commandSet.register(Command("right", "Turn right ```angle``` degrees\n", 1, [int], call.right))

commandSet.register(Command("left", "Turn left 90 degrees", 0, [], call.left, [90]))
commandSet.register(Command("left", "Turn left ```angle``` degrees\n", 1, [int], call.left))

commandSet.register(Command("random", "Plot 20 random lines", 0, [], call.random, [20]))
commandSet.register(Command("random", "Plot ```number``` random lines", 1, [int], call.random))

commandSet.register(Command("color", "Set pen to ```color```", 1, [str], call.color))
commandSet.register(Command("bgcolor", "Set background to ```color```", 1, [str], call.bgcolor))
commandSet.alias("bgcolor", "bg")
commandSet.register(Command("shape", "List pen shapes", 0, [], call.shapes))
commandSet.register(Command("shape", "Set pen shape to ```shape```\n", 1, [str], call.shape))

commandSet.register(Command("goto", "Move pen to (```x```, ```y```)\n", 2, [int, int], call.goto))

commandSet.register(Command("pos", "Show pen's position", 0, [], call.pos))
commandSet.register(Command("heading", "Show pen's heading", 0, [], call.heading))

commandSet.register(Command("reset", "Reset everything\n", 0, [], call.reset))

commandSet.register(Command("quit", "Close the canvas\n", 0, [], quit_callback))
commandSet.alias("quit", "exit")

###########
# Run GUI #
###########

print("Type `help` for help")


while kg:
    com = input(">> ")
    try:
        commandSet.execute(com)
    except InvalidCommandError as e:
        problem = "Something went wrong while executing that command:\n\t"
        problem += error_string(e)
        print(error(problem))
