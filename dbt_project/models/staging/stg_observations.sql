SELECT
    cast("DATE" as date)as date,
    "PATIENT" as patient_id,
    "ENCOUNTER" as encounter_id,
    "CATEGORY" as category,
    "CODE" as code,
    "DESCRIPTION" as description,
    "VALUE" as value,
    "UNITS" as units,
    "TYPE" as type
FROM {{source("raw","raw_observations")}}