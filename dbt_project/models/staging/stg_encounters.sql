SELECT
    "Id" as encounter_id,
    "PATIENT" as patient_id,
    "ORGANIZATION" as organization_id,
    "PROVIDER" as provider_id,
    "PAYER" as payer_id,
    cast("START" as timestamp) as start,
    cast("STOP" as timestamp) as stop,
    cast("BASE_ENCOUNTER_COST" as numeric) as base_encounter_cost,
    cast("TOTAL_CLAIM_COST" as numeric) as total_claim_cost,
    cast("PAYER_COVERAGE" as numeric) as payer_coverage,
    "CODE" as code,
    "ENCOUNTERCLASS" as encounter_class,
    "DESCRIPTION" as description,
    "REASONCODE" as reason_code,
    "REASONDESCRIPTION" as reason_description
FROM {{ source("raw", "raw_encounters") }}