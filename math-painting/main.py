"""Math Painting: asks for a canvas and shapes in the terminal,
then saves an image with the shapes drawn on it."""

from canvas import Canvas
from colors import parse_color
from shapes import Rectangle, Square


def ask_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
        except ValueError:
            pass
        print(f"Please enter a whole number of {minimum} or more.")


def ask_color(prompt):
    while True:
        try:
            return parse_color(input(prompt))
        except ValueError as error:
            print(error)


def warn_if_outside(shape_name, x, y, canvas):
    if x >= canvas.width or y >= canvas.height:
        print(f"Note: this {shape_name} starts outside the {canvas.width} x {canvas.height} canvas, so it won't be visible.")


print("Math Painting")
print("Coordinates start at the top-left corner: x goes right, y goes down.")
print("Colors can be a name (red, blue, ...) or R, G, B numbers, e.g. 255, 0, 0.\n")

width = ask_int("Canvas width in pixels: ", 1)
height = ask_int("Canvas height in pixels: ", 1)
color = ask_color("Canvas color (e.g. white or black): ")
canvas = Canvas(width, height, color)

shapes_drawn = 0
while True:
    choice = input("\nWhat would you like to draw? (square / rectangle / quit): ").strip().lower()
    if choice in ("quit", "q", ""):
        break
    if choice in ("square", "s"):
        name = "square"
        x = ask_int("x of the top-left corner: ")
        y = ask_int("y of the top-left corner: ")
        side = ask_int("Side length: ", 1)
        shape = Square(x, y, side, ask_color("Square color: "))
    elif choice in ("rectangle", "r"):
        name = "rectangle"
        x = ask_int("x of the top-left corner: ")
        y = ask_int("y of the top-left corner: ")
        rect_width = ask_int("Width: ", 1)
        rect_height = ask_int("Height: ", 1)
        shape = Rectangle(x, y, rect_width, rect_height, ask_color("Rectangle color: "))
    else:
        print("Please type square, rectangle or quit.")
        continue
    warn_if_outside(name, x, y, canvas)
    shape.draw(canvas)
    shapes_drawn += 1

imagepath = input("\nSave the image as (default: images/painting.png): ").strip() or "images/painting.png"
path = canvas.make(imagepath)
print(f"Saved {path} with {shapes_drawn} shape(s) on a {canvas.width} x {canvas.height} canvas.")
