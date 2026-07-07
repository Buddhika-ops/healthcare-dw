SELECT
    "Id" as payer_id,
    "NAME" as payer_name,
    "OWNERSHIP" as ownership,
    cast("AMOUNT_COVERED" as numeric) as amount_covered,
    cast("AMOUNT_UNCOVERED" as numeric) as amount_uncovered,
    cast("REVENUE" as numeric) as revenue,
    "COVERED_ENCOUNTERS" as covered_encounters,
    "UNCOVERED_ENCOUNTERS" as uncovered_encounters,
    "COVERED_MEDICATIONS" as covered_medications,
    "UNCOVERED_MEDICATIONS" as uncovered_medications,
    "COVERED_PROCEDURES" as covered_procedures,
    "UNCOVERED_PROCEDURES" as uncovered_procedures,
    "COVERED_IMMUNIZATIONS" as covered_immunizations,
    "UNCOVERED_IMMUNIZATIONS" as uncovered_immunizations,
    "UNIQUE_CUSTOMERS" as unique_customers,
    "QOLS_AVG" as qols_avg,
    "MEMBER_MONTHS" as member_months
FROM {{ source("raw","raw_payers") }}