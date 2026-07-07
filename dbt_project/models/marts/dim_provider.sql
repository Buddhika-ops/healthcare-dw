with provider as (
    select * from {{ ref('stg_providers') }}
),

organization as (
    select * from {{ ref('stg_organizations') }}
),

final as (
    select
        p.provider_id,
        p.organization_id,
        o.organization_name,
        p.provider_name,
        p.gender,
        p.speciality,
        p.city,
        p.state

    from provider as p
    left join organization as o
        on p.organization_id = o.organization_id
)
select * from final