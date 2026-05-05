from app.config.log_config import logger
from app.exceptions.custom_exceptions import InvalidRegimeError, AppError
from app.config.log_config import logger

class TaxCalculator:
    """Service class to calculate income tax based on regime."""

    def __init__(self, income: float, hra: float, regime: str):
        """Initialize TaxCalculator.

        Args:
            income (float): Total annual income.
            hra (float): House Rent Allowance.
            regime (str): Tax regime ("old" or "new").
        """
        self.income = income
        self.hra = hra
        self.regime = regime.lower()

    def calculate(self) -> float:
        """Calculate total tax based on regime.

        Returns:
            float: Calculated tax amount.

        Raises:
            InvalidRegimeError: If regime is invalid.
            CalculationError: If unexpected error occurs.
        """
        logger.info(f"Calculating tax for income={self.income}")
        taxable_income = self._get_taxable_income()

        if self.regime == "old":
            tax = self._calculate_old_regime(taxable_income)
            tax = self._apply_rebate_old(taxable_income, tax)

        elif self.regime == "new":
            tax = self._calculate_new_regime(taxable_income)
            tax = self._apply_rebate_new(taxable_income, tax)

        else:
            raise InvalidRegimeError()

        return round(tax, 2)
    
    def _get_taxable_income(self):
        """Compute taxable income after deductions.

        Returns:
            float: Taxable income (non-negative).
        """
        if self.regime == "old":
            standard_deduction = 50000
        else:
            standard_deduction = 75000

        taxable_income = self.income - self.hra - standard_deduction
        return max(taxable_income, 0)
    
    def _calculate_old_regime(self, income):
        """Calculate tax under old regime slabs.

        Args:
            income (float): Taxable income.

        Returns:
            float: Calculated tax.
        """
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
        """Calculate tax under new regime slabs.

        Args:
            income (float): Taxable income.

        Returns:
            float: Calculated tax.
        """
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
        """Apply rebate under old regime.

        Args:
            income (float): Taxable income.
            tax (float): Calculated tax.

        Returns:
            float: Final tax after rebate.
        """
        if income <= 500000:
            return 0
        return tax

    def _apply_rebate_new(self, income, tax):
        """Apply rebate under new regime.

        Args:
            income (float): Taxable income.
            tax (float): Calculated tax.

        Returns:
            float: Final tax after rebate.
        """
        if income <= 1200000:
            return 0
        return tax