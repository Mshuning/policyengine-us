from policyengine_us.model_api import *


class mi_standard_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "Michigan standard deduction"
    unit = USD
    definition_period = YEAR
    documentation = "Michigan standard deduction for age 67-76."
    reference = (
        "https://www.michigan.gov/taxes/iit/retirement-and-pension-benefits/michigan-standard-deduction",
        "https://www.michigan.gov/taxes/-/media/Project/Websites/taxes/Forms/2022/2022-IIT-Forms/BOOK_MI-1040.pdf?rev=86a928564e3f42449c531309673f5da7&hash=7147C48E7C9B1B8171B72DC34A66642A",
    )
    defined_for = StateCode.MI

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.mi.tax.income.deductions.standard
        # Core deduction based on filing status.
        filing_status = tax_unit("filing_status", period)

        age_older = max_(
            tax_unit("age_head", period), tax_unit("age_spouse", period)
        )
        # Michigan Standard Deduction
        sd_birth_year = -(age_older - period.start.year)
        sd_age_eligibility = (
            (age_older >= p.min_age) & (sd_birth_year >= p.birth_year)
        ).astype(int)
        sd_amount_per_aged = p.amount[filing_status]
        standrad_deduction = sd_age_eligibility * sd_amount_per_aged

        return standrad_deduction
