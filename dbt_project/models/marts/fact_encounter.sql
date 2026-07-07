select
    e.encounter_id,
    e.patient_id,
    e.organization_id as facility_id,
    e.provider_id,
    e.payer_id as insurance_plan_id,
    cast( e.start as date) as encounter_date,
    e.code,
    e.encounter_class,
    e.description,
    e.reason_code,
    e.reason_description,
    e.base_encounter_cost,
    e.total_claim_cost,
    e.payer_coverage,

    extract(epoch from(e.stop - e.start))/3600 as length_of_stay_hours
from {{ ref('stg_encounters') }} as e