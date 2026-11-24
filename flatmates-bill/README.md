# Flatmates Bill

An app that takes the amount of a bill for a period and the days each flatmate stayed in the house, returns how much each flatmate has to pay, and generates a PDF report with the names, the period and each person's share.

## Design

From [`design.txt`](design.txt):

| Object | Attributes | Methods |
|--------|------------|---------|
| `Bill` | `amount`, `period` | |
| `Flatmate` | `name`, `days_in_house` | `pays(bill, flatmate2)` |
| `PdfReport` | `filename` | `generate(flatmate1, flatmate2, bill)` |

`pays` needs the other flatmate as well as the bill, because a share depends on the total days of both:

```
pays = bill amount × (my days ÷ (my days + other flatmate's days))
```

Example: a 120.00 bill for March 2026, Saeii stayed 20 days and Mahi 25:

| Flatmate | Days | Share | Pays   |
|----------|-----:|------:|-------:|
| Saeii    |   20 | 44.4% |  53.33 |
| Mahi     |   25 | 55.6% |  66.67 |
| **Total**|   45 |  100% | 120.00 |

In the report and on the web page, the second flatmate pays the rest of the bill, so the two shares always add up exactly.

## Files

| File | Purpose |
|------|---------|
| `flat.py` | `Bill` and `Flatmate` classes |
| `reports.py` | `PdfReport` class (uses [fpdf2](https://py-pdf.github.io/fpdf2/)) |
| `main.py` | Command-line version |
| `app.py`, `templates/`, `static/` | Web version ([Flask](https://flask.palletsprojects.com/)) |
| `tests/` | Tests for the split, the PDF and the web pages |

## Run it

Set up once, from this folder:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

**Web version.** Start the server, then open http://127.0.0.1:5000:

```bash
python app.py
```

Fill in the form, click **Calculate** to see the split, or **Download PDF report** to get the PDF.

**Command-line version.** Answer the questions; the PDF is saved to `reports/<period>.pdf`:

```bash
python main.py
```

**Tests:**

```bash
pip install pytest
```

```bash
python -m pytest tests
```
