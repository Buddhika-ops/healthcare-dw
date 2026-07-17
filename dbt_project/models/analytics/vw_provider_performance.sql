select 
    d.year,
    d.month,
    f.provider_id,
    pr.provider_name,
    pr.speciality,
    count(*) as encounter_count,
    sum(f.total_claim_cost) as total_revanue
from {{ ref('fact_encounter') }} as f
left join {{ ref('dim_provider') }} as pr
on f.provider_id = pr.provider_id
left join {{ ref('dim_date') }} as d
on f.encounter_date = d.date_day
where f.encounter_date >= '2010-01-01'
group by d.year, d.month,f.provider_id, pr.speciality, pr.provider_name
order by d.year desc, d.month desc, pr.provider_name
