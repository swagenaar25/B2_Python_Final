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
__all__ = ["TurtleCallbacks"]

import typing
import turtle
import random
import math
from helpers import random_color


class TurtleCallbacks:
    """Controller for a turtle, use with commands"""
    MINIMUM_BRANCH_LENGTH = 5

    def __init__(self, pen: turtle.RawTurtle, screen: turtle.TurtleScreen, output: typing.Callable[[str], None], reset_console: typing.Callable[[None], None]):
        """Initialize callbacks

        :param pen: Turtle object to control
        :param screen: Screen object to control
        :param output: Callable for output
        :param reset_console: Callable to reset console
        """
        self.pen = pen
        self.screen = screen
        self.output = output
        self.reset_console = reset_console

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

    def clear(self):
        self.reset_console()

    # Fractals
    def tree_fractal(self, branch_length, shorten_by, angle):
        if branch_length > self.MINIMUM_BRANCH_LENGTH:
            self.pen.forward(branch_length)
            new_length = branch_length - shorten_by
            self.pen.left(angle)
            self.tree_fractal(new_length, shorten_by, angle)
            self.pen.right(angle * 2)
            self.tree_fractal(new_length, shorten_by, angle)
            self.pen.left(angle)
            self.pen.backward(branch_length)

    def koch_line(self, branch_length: float, scale: float):  # shorten by 1/3 every time
        if branch_length > 3:
            # ___
            self.koch_line(branch_length / 3, scale)
            self.pen.left(60)  # /
            self.koch_line(branch_length / 3, scale)
            self.pen.right(120)  # \
            self.koch_line(branch_length / 3, scale)
            self.pen.left(60)  # ___
            self.koch_line(branch_length / 3, scale)
        else:
            self.pen.forward(branch_length*scale)

    def _koch_snowflake(self, branch_length: float, sides: int, scale: float):
        start_pos = self.pen.pos()
        start_heading = self.pen.heading()
        sum_of_interior = (sides - 2) * 180
        interior_angle = sum_of_interior / sides
        self.pen.setheading(90 + (180 / sides) + start_heading)
        self.pen.penup()
        radius = (branch_length * scale) / (2 * math.sin(math.pi / sides))  # Center
        self.pen.forward(radius)
        self.pen.pendown()
        self.pen.setheading(0 + start_heading)
        for _ in range(sides):
            # t.forward(branch_length)
            self.koch_line(branch_length, scale)
            self.pen.right(180 - interior_angle)
        # Reset
        self.pen.penup()
        self.pen.goto(*start_pos)
        self.pen.setheading(start_heading)
        self.pen.pendown()

    def koch_snowflake(self, sides: int, depth: int, scale: float = 1.0):
        self._koch_snowflake(3**depth, sides, scale)
