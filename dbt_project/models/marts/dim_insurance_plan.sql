with payers as (
    select * from {{ ref('stg_payers') }}
),

final as (
    select
        payer_id as insurance_plan_id,
        payer_name as insurance_plan_name,
        ownership,
        amount_covered,
        amount_uncovered,
        revenue,
        covered_medications,
        uncovered_medications,
        covered_procedures,
        uncovered_procedures,
        covered_immunizations,
        uncovered_immunizations,
        unique_customers,
        qols_avg,
        member_months

    from payers
)
select * from final