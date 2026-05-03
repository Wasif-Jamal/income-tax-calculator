class TaxCalculator:

    def __init__(self, income: float, hra: float, regime: str):
        self.income = income
        self.hra = hra
        self.regime = regime.lower()

    def calculate(self) -> float:
        try:
            taxable_income = self._get_taxable_income()

            if self.regime == "old":
                tax = self._calculate_old_regime(taxable_income)
                tax = self._apply_rebate_old(taxable_income, tax)

            elif self.regime == "new":
                tax = self._calculate_new_regime(taxable_income)
                tax = self._apply_rebate_new(taxable_income, tax)

            else:
                raise ValueError("Invalid regime")

            return round(tax, 2)
        
        except ValueError:
            raise

        except Exception as e:
            raise ValueError(f'Unexpected error during tax calculation: {str(e)}')
    
    def _get_taxable_income(self):
        if self.regime == "old":
            standard_deduction = 50000
        else:
            standard_deduction = 75000

        taxable_income = self.income - self.hra - standard_deduction
        return max(taxable_income, 0)
    
    def _calculate_old_regime(self, income):
        tax = 0

        if income > 1000000:
            tax += (income - 1000000) * 0.3
            income = 1000000

        if income > 500000:
            tax += (income - 500000) * 0.2
            income = 500000

        if income > 250000:
            tax += (income - 250000) * 0.05

        return tax
    
    def _calculate_new_regime(self, income):
        tax = 0

        slabs = [
            (2400000, 0.30),
            (2000000, 0.25),
            (1600000, 0.20),
            (1200000, 0.15),
            (800000, 0.10),
            (400000, 0.05),
        ]

        for limit, rate in slabs:
            if income > limit:
                tax += (income - limit) * rate
                income = limit

        return tax
    
    def _apply_rebate_old(self, income, tax):
        if income <= 500000:
            return 0
        return tax

    def _apply_rebate_new(self, income, tax):
        if income <= 1200000:
            return 0
        return tax