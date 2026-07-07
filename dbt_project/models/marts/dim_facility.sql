select
    organization_id,
    organization_name,
    city,
    state,
    revenue,
    utilization

from {{ ref('stg_organizations') }}