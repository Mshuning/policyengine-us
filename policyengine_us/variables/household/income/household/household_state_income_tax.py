from policyengine_us.model_api import *


class household_state_income_tax(Variable):
    # This definition contains all modelled states, and exists to solve circular dependencies in state_income_tax.
    value_type = float
    entity = TaxUnit
    label = "household State tax"
    unit = USD
    definition_period = YEAR
    exhaustive_parameter_dependencies = "gov.states"

    def formula(tax_unit, period, parameters):
        if parameters(period).simulation.reported_state_income_tax:
            spm_unit = tax_unit.spm_unit
            total_tax_unit_heads = add(spm_unit, period, ["is_tax_unit_head"])
            spm_unit_state_tax = spm_unit(
                "spm_unit_state_tax_reported", period
            )
            return where(
                total_tax_unit_heads > 0,
                spm_unit_state_tax / total_tax_unit_heads,
                0,
            )
        else:
            p = parameters(period)
            return add(
                tax_unit, period, p.gov.household_state_income_tax
            ) - add(tax_unit, period, p.gov.state_refundable_credits)
