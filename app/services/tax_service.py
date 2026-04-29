def calculate_tax(income: float, hra: float, regime: str) -> float:
    taxable_income = income - hra

    if regime == "old":
        if taxable_income <= 250000:
            return 0
        elif taxable_income <= 500000:
            return taxable_income * 0.05
        elif taxable_income <= 1000000:
            return taxable_income * 0.2
        else:
            return taxable_income * 0.3

    elif regime == "new":
        if taxable_income <= 400000:
            return 0
        elif taxable_income <= 800000:
            return taxable_income * 0.05
        elif taxable_income <= 1200000:
            return taxable_income * 0.1
        elif taxable_income <= 1600000:
            return taxable_income * 0.2
        elif taxable_income <= 2000000:
            return taxable_income * 0.25
        else:
            return taxable_income * 0.3

    else:
        raise ValueError("Invalid regime")