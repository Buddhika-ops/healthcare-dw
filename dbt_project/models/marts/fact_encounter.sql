with encounter as(
    select * from {{ ref('stg_encounters') }}
),

final as (
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

        case
            when e.stop is null then null
            else (cast(e.stop as date) - cast(e.start as date)) * 24
        end as length_of_stay_hours

        from encounter as e
)

select * from final
