import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from canvas import Canvas  # noqa: E402
from colors import parse_color  # noqa: E402
from shapes import Rectangle, Square  # noqa: E402

RED, BLUE, WHITE = (255, 0, 0), (0, 0, 255), (255, 255, 255)


def test_canvas_is_filled_with_its_color():
    canvas = Canvas(30, 20, WHITE)
    assert canvas.data.shape == (20, 30, 3)
    assert (canvas.data == WHITE).all()


def test_square_covers_exactly_its_area():
    canvas = Canvas(50, 50, WHITE)
    Square(10, 20, 5, RED).draw(canvas)
    painted = np.argwhere((canvas.data == RED).all(axis=2))
    assert len(painted) == 25
    # rows are y, columns are x
    assert painted.min(axis=0).tolist() == [20, 10]
    assert painted.max(axis=0).tolist() == [24, 14]


def test_rectangle_uses_width_along_x_and_height_along_y():
    canvas = Canvas(100, 100, WHITE)
    Rectangle(5, 10, 40, 8, BLUE).draw(canvas)
    painted = np.argwhere((canvas.data == BLUE).all(axis=2))
    assert len(painted) == 40 * 8
    assert painted.max(axis=0).tolist() == [17, 44]


def test_shape_past_the_edge_is_cut_off():
    canvas = Canvas(10, 10, WHITE)
    Square(8, 8, 5, RED).draw(canvas)
    assert (canvas.data == RED).all(axis=2).sum() == 4


def test_later_shapes_paint_over_earlier_ones():
    canvas = Canvas(10, 10, WHITE)
    Square(0, 0, 10, RED).draw(canvas)
    Rectangle(2, 2, 2, 2, BLUE).draw(canvas)
    assert tuple(canvas.data[3, 3]) == BLUE and tuple(canvas.data[0, 0]) == RED


def test_make_saves_the_image(tmp_path):
    canvas = Canvas(40, 30, (0, 0, 0))
    Square(0, 0, 10, RED).draw(canvas)
    path = canvas.make(tmp_path / "out" / "painting.png")
    image = Image.open(path)
    assert image.size == (40, 30)
    assert image.getpixel((5, 5)) == RED and image.getpixel((20, 20)) == (0, 0, 0)


@pytest.mark.parametrize("text, expected", [
    ("white", WHITE), (" Red ", (220, 40, 40)), ("255, 0, 0", RED), ("0 0 255", BLUE),
])
def test_parse_color(text, expected):
    assert parse_color(text) == expected


@pytest.mark.parametrize("text", ["sky", "256,0,0", "1,2"])
def test_parse_color_rejects_bad_input(text):
    with pytest.raises(ValueError):
        parse_color(text)


def test_invalid_shapes_are_rejected():
    with pytest.raises(ValueError):
        Square(-1, 0, 5, RED)
    with pytest.raises(ValueError):
        Rectangle(0, 0, 0, 5, RED)
    with pytest.raises(ValueError):
        Canvas(0, 10)
