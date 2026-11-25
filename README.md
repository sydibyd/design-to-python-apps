# design-to-python-apps

Practicing app design and development from scratch with AI. Each folder is one Python app: the original design file (objects, attributes, methods), the code built from it, and a README on how to run it.

## How each app is built

1. **Design**: a plain-text `design.txt` names the app, describes what it does, and lists its objects with their attributes and methods.
2. **Build**: the objects become Python classes with the same names, then a `main.py` runs the app from the terminal.
3. **Test**: each app has tests in `tests/` that check the core logic.

## Apps

| App | What it does | Run it |
|-----|--------------|--------|
| [Flatmates Bill](flatmates-bill) | Splits a shared bill between two flatmates by days spent in the house and generates a PDF report | `python main.py` |
| [Math Painting](math-painting) | Draws squares and rectangles from coordinates, sizes and colors you type, and saves the result as an image | `python main.py` |

## Running an app

Each app has its own `requirements.txt`. From the app's folder:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Then follow the app's README.
