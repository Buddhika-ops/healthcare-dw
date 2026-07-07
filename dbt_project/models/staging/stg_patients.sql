SELECT
    "Id" as patient_id,
    cast("BIRTHDATE" as date)as birth_date,
    cast("DEATHDATE" as date)as death_date,
    "GENDER" as gender,
    "RACE" as race,
    "ETHNICITY" as ethnicity,
    "MARITAL" as marital,
    "CITY" as city,
    "STATE" as state,
    "ZIP" as zip_code,
    cast("INCOME" as numeric) as income,
    cast("HEALTHCARE_COVERAGE" as numeric) as healthcare_coverage,
    cast("HEALTHCARE_EXPENSES" as numeric) as healthcare_expenses

FROM {{source("raw","raw_patients")}}