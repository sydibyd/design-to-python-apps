"""Square and Rectangle objects, as described in design.txt.

Coordinates start at the top-left corner of the canvas: x goes right, y goes down.
(x, y) is the shape's top-left corner. A shape that reaches past the edge of the
canvas is cut off at the edge.
"""


def _check(x, y, *sizes):
    if x < 0 or y < 0:
        raise ValueError("x and y must be 0 or more.")
    if any(size <= 0 for size in sizes):
        raise ValueError("Sizes must be greater than zero.")


class Rectangle:
    def __init__(self, x, y, width, height, color):
        _check(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, canvas):
        """Paint the rectangle onto the canvas."""
        canvas.data[self.y:self.y + self.height, self.x:self.x + self.width] = self.color


class Square:
    def __init__(self, x, y, side, color):
        _check(x, y, side)
        self.x = x
        self.y = y
        self.side = side
        self.color = color

    def draw(self, canvas):
        """Paint the square onto the canvas."""
        canvas.data[self.y:self.y + self.side, self.x:self.x + self.side] = self.color
