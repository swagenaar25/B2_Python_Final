__all__ = ["TurtleCallbacks"]

import typing
import turtle
import random
from helpers import random_color


class TurtleCallbacks:
    """Controller for a turtle, use with commands"""
    def __init__(self, pen: turtle.RawTurtle, screen: turtle.TurtleScreen, output: typing.Callable[[str], None]):
        """Initialize callbacks

        :param pen: Turtle object to control
        :param screen: Screen object to control
        :param output: Callable for output
        """
        self.pen = pen
        self.screen = screen
        self.output = output

    def penup(self):
        self.pen.penup()

    def pendown(self):
        self.pen.pendown()

    def forward(self, distance: int):
        self.pen.forward(distance)

    def back(self, distance: int):
        self.pen.back(distance)

    def right(self, angle: float):
        self.pen.right(angle)

    def left(self, angle: float):
        self.pen.left(angle)

    def random(self, number: int):
        original_color = self.pen.color()[0]
        for _ in range(number):
            self.pen.color(random_color())
            x = random.randint(0, self.screen.canvwidth) - (self.screen.canvwidth/2)
            y = random.randint(0, self.screen.canvheight) - (self.screen.canvheight/2)
            self.pen.goto(x, y)
        self.pen.color(original_color)

    def shape(self, shape: str):
        self.pen.shape(shape)

    def color(self, color: str):
        self.pen.color(color)

    def bgcolor(self, color: str):
        self.screen.bgcolor(color)

    def goto(self, x: int, y: int):
        self.pen.goto(x, y)

    def pos(self):
        self.output(f"Turtle position: {self.pen.pos()}")

    def heading(self):
        self.output(f"Turtle heading: {self.pen.heading()}")

    def shapes(self):
        self.output(f"Available shapes: {self.screen.getshapes()}")

    def reset(self):
        self.screen.reset()
