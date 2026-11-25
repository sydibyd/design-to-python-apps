"""Canvas object, as described in design.txt."""

from pathlib import Path

import numpy as np
from PIL import Image


class Canvas:
    """An image of width x height pixels filled with one background color.

    The pixels are stored in self.data, a NumPy array of shape (height, width, 3):
    one row per y, one column per x, and an (R, G, B) value in each cell.
    """

    def __init__(self, width, height, color=(255, 255, 255)):
        if width <= 0 or height <= 0:
            raise ValueError("The canvas width and height must be greater than zero.")
        self.width = width
        self.height = height
        self.color = color
        self.data = np.zeros((height, width, 3), dtype=np.uint8)
        self.data[:] = color

    def make(self, imagepath):
        """Save the canvas as an image file (PNG, JPG, ...) and return its path."""
        path = Path(imagepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(self.data).save(path)
        return path
