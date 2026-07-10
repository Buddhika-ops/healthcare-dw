with observations as (
    select * from {{ ref('stg_observations') }}
),

final as (
    select
       md5( concat(patient_id,'-' ,encounter_id,'-',cast(date as varchar))) as lab_result_id,
        patient_id,
        encounter_id,
        category,
        date as result_date,
        code,
        description,
        value,
        units,
        type as value_types

    from observations
    where category = 'laboratory'
)

select * from final