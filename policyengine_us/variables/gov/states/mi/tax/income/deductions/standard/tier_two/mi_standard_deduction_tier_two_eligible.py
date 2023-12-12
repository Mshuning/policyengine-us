from policyengine_us.model_api import *


class mi_standard_deduction_tier_two_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Eligible for the Michigan tier two standard deduction"
    definition_period = YEAR
    reference = (
        "http://legislature.mi.gov/doc.aspx?mcl-206-30",  # (9)(b) & (c)
        "https://www.michigan.gov/taxes/iit/retirement-and-pension-benefits/michigan-standard-deduction",
        "https://www.michigan.gov/taxes/-/media/Project/Websites/taxes/Forms/2022/2022-IIT-Forms/BOOK_MI-1040.pdf#page=15",
    )
    defined_for = StateCode.MI

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.mi.tax.income.deductions.standard.tier_two

        older_spouse_birth_year = tax_unit("older_spouse_birth_year", period)
     
        return p.birth_year.calc(older_spouse_birth_year)
