SELECT
    "Id" as patient_id,
    CAST(NULLIF("BIRTHDATE", 'NaN') AS date) as birth_date,
    CAST(NULLIF("DEATHDATE", 'NaN') AS date) as death_date,
    "GENDER" as gender,
    "RACE" as race,
    "ETHNICITY" as ethnicity,
    "MARITAL" as marital,
    "CITY" as city,
    "STATE" as state,
    "ZIP" as zip_code,
    CAST(NULLIF("INCOME"::text, 'NaN') AS numeric) as income,
    CAST(NULLIF("HEALTHCARE_COVERAGE", 'NaN') AS numeric) as healthcare_coverage,
    CAST(NULLIF("HEALTHCARE_EXPENSES", 'NaN') AS numeric) as healthcare_expenses

FROM {{ source("raw","raw_patients") }}