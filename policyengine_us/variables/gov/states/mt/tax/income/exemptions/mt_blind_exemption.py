from policyengine_us.model_api import *


class mt_blind_exemption(Variable):
    value_type = float
    entity = TaxUnit
    label = "Montana blind exemption"
    unit = USD
    definition_period = YEAR
    reference = "https://regulations.justia.com/states/montana/department-42/chapter-42-15/subchapter-42-15-4/rule-42-15-402/"
    defined_for = StateCode.MT

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.mt.tax.income.exemptions
        # Count number of is_blind from tax_unit
        blind_head = tax_unit("blind_head", period).astype(int)
        blind_spouse = tax_unit("blind_spouse", period).astype(int)
        return (blind_head + blind_spouse) * p.amount
