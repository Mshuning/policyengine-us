from policyengine_us.model_api import *


class tax_unit_parents(Variable):
    value_type = int
    entity = TaxUnit
    label = "Number of parents in the tax unit"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        return add(tax_unit, period, ["is_parent"])
