from policyengine_us.model_api import *


class mo_property_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "MO property tax credit"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://dor.mo.gov/forms/MO-PTS_2021.pdf",
        "https://revisor.mo.gov/main/OneSection.aspx?section=135.010&bid=6435",
        "https://revisor.mo.gov/main/OneSection.aspx?section=135.030&bid=6439",
    )
    defined_for = StateCode.MO

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.mo.tax.income.credits.property_tax
        # compute maximum (that is, pre-phaseout) credit amount for rent
        rent = add(tax_unit, period, ["rent"])
        ratio = p.property_tax_rent_ratio
        rent_limit = p.rent_property_tax_limit
        rent_amount = min_(rent * ratio, rent_limit)
        # compute maximum (that is, pre-phaseout) credit amount for taxes
        ptax = add(tax_unit, period, ["real_estate_taxes"])
        ptax_limit = p.property_tax_limit
        ptax_amount = min_(ptax, ptax_limit)
        # combine the rent_amount and ptax_amount subject to ptax_limit
        max_credit = min_(rent_amount + ptax_amount, ptax_limit)
        # phase out credit amount using legislative formula (not form table)
        po_start = p.phaseout_threshold
        po_rate = p.phaseout_rate
        excess_income = tax_unit("mo_ptc_net_income", period) - po_start
        phaseout_amount = po_rate * max(0, excess_income)
        credit = max_(0, max_credit - phaseout_amount)
        # allow credit only for eligible tax units        
        eligible = tax_unit("mo_ptc_taxunit_eligibility", period)
        return eligible * credit
