from policyengine_us.model_api import *


class retirement_saving_eligible_person(Variable):
    entity = Person
    definition_period = YEAR
    label = "Eligible person for the retirement saving contributions credit"
    value_type = bool
    reference = "https://www.irs.gov/pub/irs-pdf/f8880.pdf"

    def formula(person, period, parameters):
        p = parameters(period).gov.irs.credits.retirement_saving
        age_eligible = person("age", period) >= p.threshold.age
        full_time_student = person("is_full_time_student", period)
        claimed_on_another_return = person(
            "claimed_as_dependent_on_another_return", period
        )
        head_or_spouse = person("is_tax_unit_head_or_spouse", period)

        return (
            age_eligible
            & head_or_spouse
            & ~full_time_student
            & ~claimed_on_another_return
        )
