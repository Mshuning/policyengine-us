from policyengine_us.model_api import *


class mi_homestead_property_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Michigan homestead property tax credit"
    unit = USD
    definition_period = YEAR
    reference = (
        "http://legislature.mi.gov/doc.aspx?mcl-206-508",
        "https://www.michigan.gov/taxes/-/media/Project/Websites/taxes/Forms/2022/2022-IIT-Forms/MI-1040CR.pdf#page=2",
    )
    defined_for = "mi_homestead_property_tax_credit_eligible"

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.mi.tax.income.credits.homestead_property_tax_credit

        total_household_resources = tax_unit("mi_household_resources", period)
        homestead_allowable = tax_unit(
            "mi_allowable_homestead_property_tax_credit", period
        )  # Line 42

        phase_out_rate = p.rate.phase_out.calc(
            total_household_resources
        )  # Line 43

        return phase_out_rate * homestead_allowable  # Line 44
