"""Bill and Flatmate objects, as described in design.txt."""


class Bill:
    """A bill for a given period.

    amount: total amount to split, e.g. 120
    period: the billing period, e.g. "March 2026"
    """

    def __init__(self, amount, period):
        if amount <= 0:
            raise ValueError("The bill amount must be greater than zero.")
        self.amount = amount
        self.period = period


class Flatmate:
    """A person living in the flat who pays a share of the bill."""

    def __init__(self, name, days_in_house):
        if days_in_house < 0:
            raise ValueError("Days in house cannot be negative.")
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatmate2):
        """Return this flatmate's share of the bill, rounded to the cent.

        Each flatmate pays in proportion to their days in the house:
        share = bill amount x (my days / total days of both flatmates)
        """
        total_days = self.days_in_house + flatmate2.days_in_house
        if total_days == 0:
            raise ValueError("At least one flatmate needs more than zero days.")
        weight = self.days_in_house / total_days
        return round(bill.amount * weight, 2)
