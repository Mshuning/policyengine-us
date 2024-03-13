from policyengine_us.model_api import *


def create_medicare_and_investment_tax_increase() -> Reform:
    class additional_medicare_tax(Variable):
        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        label = "Additional Medicare Tax"
        unit = USD
        documentation = (
            "Additional Medicare Tax from Form 8959 (included in payrolltax)"
        )

        def formula(tax_unit, period, parameters):
            amc = parameters(period).gov.irs.payroll.medicare.additional
            # Wage and self-employment income are taxed the same.
            ELEMENTS = ["irs_employment_income", "taxable_self_employment_income"]
            wages_plus_se = add(tax_unit, period, ELEMENTS)
            exclusion = amc.exclusion[tax_unit("filing_status", period)]
            base = max_(0, wages_plus_se - exclusion)
            base_tax = amc.rate * base
            p_ref = parameters(period).gov.contrib.treasury.budget.medicare
            add_tax = p_ref.rate.calc(wages_plus_se)
            print(base_tax)
            print(wages_plus_se)
            print(add_tax)
            return base_tax + add_tax


    class net_investment_income_tax(Variable):
        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        label = "Net Investment Income Tax"
        reference = "https://www.law.cornell.edu/uscode/text/26/1411"
        unit = USD

        def formula(tax_unit, period, parameters):
            p = parameters(period).gov.irs.investment.net_investment_income_tax
            threshold = p.threshold[tax_unit("filing_status", period)]
            agi = tax_unit("adjusted_gross_income", period)
            excess_agi = max_(
                0, agi - threshold
            )
            base = min_(
                max_(0, tax_unit("net_investment_income", period)),
                excess_agi,
            )
            base_tax = p.rate * base
            p_ref = parameters(period).gov.contrib.treasury.budget.net_investment_income
            add_tax = p_ref.rate.calc(agi)
            return base_tax + add_tax


    class reform(Reform):
        def apply(self):
            self.update_variable(additional_medicare_tax)
            self.update_variable(net_investment_income_tax)
    return reform


def create_medicare_and_investment_tax_increase_reform(
    parameters, period, bypass: bool = False
):
    if bypass:
        return create_medicare_and_investment_tax_increase()

    p = parameters(period).gov.contrib.treasury.budget

    if (p.medicare.rate.rates[-1] > 0) | (p.net_investment_income.rate.rates[-1] > 0):
        return create_medicare_and_investment_tax_increase()
    else:
        return None


medicare_and_investment_tax_increase = create_medicare_and_investment_tax_increase_reform(
    None, None, bypass=True
)
