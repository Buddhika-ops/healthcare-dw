with organizations as (
    select * from {{ ref('stg_organizations') }}
),

final as (   
     select
        organization_id as facility_id,
        organization_name as facility_name,
        city,
        state,
        revenue,
        utilization

    from stg_organizations
)
select * from final