"""Web version: a Flask app with a form, the results and a PDF download."""

import tempfile
from io import BytesIO
from pathlib import Path

from flask import Flask, render_template, request, send_file

from flat import Bill, Flatmate
from reports import PdfReport

app = Flask(__name__)

EXAMPLE = {"amount": "120", "period": "March 2026",
           "name1": "Saeii", "days1": "20", "name2": "Mahi", "days2": "25"}


def read_form(data):
    """Turn form fields into (bill, flatmate1, flatmate2), or raise ValueError
    with a message the user can act on."""
    try:
        amount = float(data.get("amount", ""))
    except ValueError:
        raise ValueError("Enter the bill amount as a number, e.g. 120.")
    period = data.get("period", "").strip()
    if not period:
        raise ValueError("Enter the bill period, e.g. March 2026.")
    mates = []
    for n in ("1", "2"):
        name = data.get(f"name{n}", "").strip()
        if not name:
            raise ValueError(f"Enter a name for flatmate {n}.")
        try:
            days = int(data.get(f"days{n}", ""))
        except ValueError:
            raise ValueError(f"Days in house for {name} must be a whole number.")
        mates.append(Flatmate(name, days))
    bill = Bill(amount, period)
    mates[0].pays(bill, mates[1])  # raises if both have zero days
    return bill, mates[0], mates[1]


@app.route("/", methods=["GET", "POST"])
def index():
    form = request.form if request.method == "POST" else EXAMPLE
    error = result = None
    try:
        bill, flatmate1, flatmate2 = read_form(form)
        pays1 = flatmate1.pays(bill, flatmate2)
        total_days = flatmate1.days_in_house + flatmate2.days_in_house
        result = {
            "bill": bill,
            "total_days": total_days,
            "rows": [
                (flatmate1, pays1),
                (flatmate2, round(bill.amount - pays1, 2)),
            ],
        }
    except ValueError as exc:
        error = str(exc)
    return render_template("index.html", form=form, error=error, result=result)


@app.route("/report", methods=["POST"])
def report():
    try:
        bill, flatmate1, flatmate2 = read_form(request.form)
    except ValueError as exc:
        return render_template("index.html", form=request.form, error=str(exc), result=None), 400
    safe_period = "".join(c if c.isalnum() else "-" for c in bill.period).strip("-").lower()
    filename = f"flatmates-bill-{safe_period or 'report'}.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        path = PdfReport(Path(tmp) / filename).generate(flatmate1, flatmate2, bill)
        data = path.read_bytes()
    return send_file(BytesIO(data), mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
