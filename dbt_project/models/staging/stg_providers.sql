SELECT
    "Id" as provider_id,
    "NAME" as provider_name,
    "GENDER" as gender,
    "ORGANIZATION" as organization_id,
    "CITY" as city,
    "STATE" as state,
    "ZIP" as zip_code,
    "ENCOUNTERS" as encounter,
    "SPECIALITY" as speciality,
    "PROCEDURES" as procedures
FROM {{ source("raw","raw_providers") }}