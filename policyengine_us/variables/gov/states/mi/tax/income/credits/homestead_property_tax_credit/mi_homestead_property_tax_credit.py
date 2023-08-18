from policyengine_us.model_api import *


class mi_homestead_property_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Michigan Homestead Property Tax Credit"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MI

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.mi.tax.income.credits.homestead_property_tax_credit

        total_household_resources = tax_unit("mi_household_resources", period)

        # seniors
        age_older = tax_unit("age_head", period)
        phase_out_rate = where(
            age_older >= p.senior.min_age,
            p.senior.phase_out_rate.calc(total_household_resources),
            p.phase_out_rate.calc(total_household_resources),
        )

        property_value = add(tax_unit, period, ["assessed_property_value"])
        rents = add(tax_unit, period, ["rent"])
        refundable_amount = tax_unit(
            "mi_homestead_property_tax_credit_refundable", period
        )

        eligibility = where(
            rents > 0,
            refundable_amount > 0,
            (refundable_amount > 0) & (property_value < p.max_property_value),
        )

        return min_(
            eligibility * refundable_amount * phase_out_rate,
            p.max_amount,
        )
