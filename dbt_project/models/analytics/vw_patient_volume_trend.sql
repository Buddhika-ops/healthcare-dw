select 
    d.year,
    d.month,
    count(*) as encounter_count

from {{ ref("fact_encounter") }} as f
left join {{ ref('dim_date') }} as d
on f.encounter_date = d.date_day

where f.encounter_date >= '2010-01-01'

group by d.year,d.month
order by d.year, d.month

