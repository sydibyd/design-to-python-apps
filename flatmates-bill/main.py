"""Command-line version: asks for the bill and the flatmates, prints
what each one pays and saves a PDF report."""

from flat import Bill, Flatmate
from reports import PdfReport


def ask_number(prompt, cast=float):
    while True:
        try:
            return cast(input(prompt))
        except ValueError:
            print("Please enter a number.")


amount = ask_number("Enter the bill amount: ")
period = input("What is the bill period? E.g. March 2026: ")

name1 = input("What is your name? ")
days1 = ask_number(f"How many days did {name1} stay in the house during the bill period? ", int)

name2 = input("What is the name of the other flatmate? ")
days2 = ask_number(f"How many days did {name2} stay in the house during the bill period? ", int)

bill = Bill(amount, period)
flatmate1 = Flatmate(name1, days1)
flatmate2 = Flatmate(name2, days2)

print(f"{flatmate1.name} pays: {flatmate1.pays(bill, flatmate2):.2f}")
print(f"{flatmate2.name} pays: {flatmate2.pays(bill, flatmate1):.2f}")

report = PdfReport(filename=f"reports/{bill.period}.pdf")
path = report.generate(flatmate1, flatmate2, bill)
print(f"PDF report saved to {path}")
