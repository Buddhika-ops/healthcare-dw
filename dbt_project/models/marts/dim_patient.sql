select
    patient_id,
    birth_date,
    death_date,
    gender,
    race,
    ethnicity,
    marital,
    city,
    state,
    zip_code,
    income,
    healthcare_expenses,
    healthcare_coverage,

    
    date_part(
        'year',
        age(coalesce(death_date, current_date), birth_date)
    ) as age

from {{ ref('stg_patients') }}