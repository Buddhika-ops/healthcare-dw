select
    p.provider_id,
    p.organization_id,
    o.organization_name,
    p.provider_name,
    p.gender,
    p.speciality,
    p.city,
    p.state

from {{ ref('stg_providers') }} as p
left join {{ ref('stg_organizations') }} as o
    on p.organization_id = o.organization_id