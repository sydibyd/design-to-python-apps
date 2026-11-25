"""Turn what the user types ("red" or "255, 0, 0") into an (R, G, B) tuple."""

NAMED_COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (220, 40, 40),
    "green": (40, 160, 70),
    "blue": (40, 90, 210),
    "yellow": (245, 200, 30),
    "orange": (240, 130, 30),
    "purple": (130, 60, 170),
    "pink": (240, 120, 170),
    "gray": (128, 128, 128),
    "brown": (130, 80, 40),
    "cyan": (40, 190, 210),
}


def parse_color(text):
    """Return an (R, G, B) tuple from a color name or three numbers from 0 to 255."""
    value = text.strip().lower()
    if value in NAMED_COLORS:
        return NAMED_COLORS[value]
    parts = value.replace(" ", ",").split(",")
    parts = [p for p in parts if p]
    if len(parts) == 3 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        return tuple(int(p) for p in parts)
    names = ", ".join(NAMED_COLORS)
    raise ValueError(f"Unknown color '{text}'. Use a name ({names}) or R, G, B numbers from 0 to 255, e.g. 255, 0, 0.")
