import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app  # noqa: E402
from flat import Bill, Flatmate  # noqa: E402
from reports import PdfReport  # noqa: E402


def test_pays_in_proportion_to_days():
    bill = Bill(120, "March 2026")
    saeii, mahi = Flatmate("Saeii", 20), Flatmate("Mahi", 25)
    assert saeii.pays(bill, mahi) == 53.33
    assert mahi.pays(bill, saeii) == 66.67


def test_equal_days_split_evenly():
    bill = Bill(100, "April 2026")
    a, b = Flatmate("A", 30), Flatmate("B", 30)
    assert a.pays(bill, b) == b.pays(bill, a) == 50


def test_zero_days_rejected():
    with pytest.raises(ValueError):
        Flatmate("A", 0).pays(Bill(100, "May"), Flatmate("B", 0))


def test_invalid_bill_rejected():
    with pytest.raises(ValueError):
        Bill(0, "May")


def test_pdf_report_is_written(tmp_path):
    path = PdfReport(tmp_path / "report.pdf").generate(
        Flatmate("Saeii", 20), Flatmate("Mahi", 25), Bill(120, "March 2026"))
    assert path.read_bytes().startswith(b"%PDF")


def test_web_page_and_pdf_download():
    client = app.test_client()
    page = client.get("/")
    assert page.status_code == 200 and b"53.33" in page.data and b"66.67" in page.data
    form = {"amount": "90", "period": "June 2026", "name1": "Saeii", "days1": "10",
            "name2": "Mahi", "days2": "20"}
    assert b"30.00" in client.post("/", data=form).data
    pdf = client.post("/report", data=form)
    assert pdf.status_code == 200 and pdf.data.startswith(b"%PDF")
    assert "flatmates-bill-june-2026.pdf" in pdf.headers["Content-Disposition"]


def test_web_form_shows_error():
    bad = {"amount": "abc", "period": "x", "name1": "a", "days1": "1", "name2": "b", "days2": "1"}
    assert b"as a number" in app.test_client().post("/", data=bad).data
