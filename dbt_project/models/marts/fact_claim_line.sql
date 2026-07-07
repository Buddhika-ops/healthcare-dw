with claim as (
    select * from {{ ref('stg_claims') }}
),

unpivoted as (
    select 
        claim_id,
        patient_id,
        provider_id,
        primary_insurance_id ,
        current_illness_date,
        service_date,
        'primary'  as responsibility_type,
        status_1 as claim_status,
        outstanding_1 as outstanding_amount
    from claim


union all


    select 
        claim_id,
        patient_id,
        provider_id,
        primary_insurance_id ,
        current_illness_date,
        service_date,
        'secondary'  as responsibility_type,
        status_2 as claim_status,
        outstanding_2 as outstanding_amount
    from claim

union all

    select 
        claim_id,
        patient_id,
        provider_id,
        primary_insurance_id, 
        current_illness_date,
        service_date,
        'patient'  as responsibility_type,
        status_p as claim_status,
        outstanding_p as outstanding_amount
    from claim

),

final as (
    select 
        md5(concat(claim_id, '-' ,responsibility_type)) as fact_claim_line_id,
        claim_id,
        patient_id,
        provider_id,
        primary_insurance_id as insurance_plan_id,
        cast(current_illness_date as date) as current_illness_date,
        cast(service_date as date) as service_date,
        responsibility_type,
        claim_status,
        coalesce(outstanding_amount,0) as outstanding_amount,
        case when coalesce(outstanding_amount ,0) > 0 then true else false end as has_outstanding_balance 

    from unpivoted
    
)

select * from final