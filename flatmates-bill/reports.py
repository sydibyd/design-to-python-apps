"""PdfReport object, as described in design.txt."""

from datetime import date
from pathlib import Path

from fpdf import FPDF

ACCENT = (13, 107, 90)
INK = (21, 32, 30)
MUTED = (91, 107, 104)


class PdfReport:
    """Creates a PDF file with the flatmates' names, the period
    and how much each of them has to pay."""

    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatmate1, flatmate2, bill):
        """Write the report to self.filename and return its path."""
        flatmate1_pays = flatmate1.pays(bill, flatmate2)
        # Flatmate 2 pays the rest, so the two shares always add up to the bill.
        flatmate2_pays = round(bill.amount - flatmate1_pays, 2)
        total_days = flatmate1.days_in_house + flatmate2.days_in_house

        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.set_margins(56, 56, 56)
        pdf.add_page()
        width = pdf.w - 2 * 56

        # Header band and title
        pdf.set_fill_color(*ACCENT)
        pdf.rect(0, 0, pdf.w, 8, style="F")
        pdf.set_y(50)
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(*INK)
        pdf.cell(width, 30, "Flatmates Bill", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*MUTED)
        pdf.cell(width / 2, 20, f"Period: {bill.period}")
        pdf.cell(width / 2, 20, f"Generated {date.today():%d %B %Y}", align="R",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*INK)
        pdf.set_line_width(1.5)
        pdf.line(56, pdf.get_y() + 6, 56 + width, pdf.get_y() + 6)
        pdf.ln(24)

        # Summary figures
        third = width / 3
        pdf.set_font("Helvetica", "B", 9)
        for label in ("BILL AMOUNT", "TOTAL DAYS", "COST PER DAY"):
            pdf.cell(third, 14, label)
        pdf.ln(16)
        pdf.set_font("Courier", "B", 15)
        pdf.set_text_color(*INK)
        pdf.cell(third, 20, f"{bill.amount:.2f}")
        pdf.cell(third, 20, str(total_days))
        pdf.cell(third, 20, f"{bill.amount / total_days:.2f}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(24)

        # Table
        cols = (width * 0.46, width * 0.16, width * 0.16, width * 0.22)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*MUTED)
        for text, w, align in zip(("FLATMATE", "DAYS", "SHARE", "PAYS"), cols, "LRRR"):
            pdf.cell(w, 18, text, align=align)
        pdf.ln(18)
        pdf.set_draw_color(211, 220, 218)
        pdf.set_line_width(0.8)
        pdf.line(56, pdf.get_y(), 56 + width, pdf.get_y())

        pdf.set_text_color(*INK)
        for mate, pays in ((flatmate1, flatmate1_pays), (flatmate2, flatmate2_pays)):
            share = mate.days_in_house / total_days * 100
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(cols[0], 30, mate.name)
            pdf.set_font("Courier", "", 12)
            pdf.cell(cols[1], 30, str(mate.days_in_house), align="R")
            pdf.cell(cols[2], 30, f"{share:.1f}%", align="R")
            pdf.set_font("Courier", "B", 12)
            pdf.cell(cols[3], 30, f"{pays:.2f}", align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.set_draw_color(*INK)
        pdf.set_line_width(1.5)
        pdf.line(56, pdf.get_y(), 56 + width, pdf.get_y())
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(cols[0], 28, "Total")
        pdf.set_font("Courier", "B", 12)
        pdf.cell(cols[1], 28, str(total_days), align="R")
        pdf.cell(cols[2], 28, "100%", align="R")
        pdf.cell(cols[3], 28, f"{flatmate1_pays + flatmate2_pays:.2f}", align="R",
                 new_x="LMARGIN", new_y="NEXT")

        pdf.ln(24)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(width, 13, "Each flatmate pays the bill amount multiplied by their days "
                                  "in the house divided by the total days of both flatmates.")

        path = Path(self.filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        return path
