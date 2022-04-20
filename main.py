"""
Author: Sam Wagenaar
Created: 4/13/2022
Modified: 4/13/2022
Purpose: Final Exam
Class: Intro to Programming
"""

import turtle
import tkinter as tk
from queue import Queue
from command_lib import Command, CommandSet, InvalidCommandError
from callbacks import TurtleCallbacks
from standard_command_set import StandardCommandSet
from helpers import error_format, error_string

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
standardCommandSet = StandardCommandSet(bob, window, quit_callback, print)

###########
# Run GUI #
###########

print("Type `help` for help")


while kg:
    com = input(">> ")
    try:
        standardCommandSet.user_input(com)
    except InvalidCommandError as e:
        problem = "[LOOP] Something went wrong while executing that command:\n\t"
        problem += error_string(e)
        print(error_format(problem))
