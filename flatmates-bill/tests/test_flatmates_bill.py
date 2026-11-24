import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
