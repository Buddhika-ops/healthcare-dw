select 
    f.facility_id,
    d.year ,
    d.month,
    fac.facility_name,  
    sum(f.total_claim_cost) as total_cost

from {{ ref('fact_encounter') }} as f

left join {{ ref('dim_facility') }} as fac
on f.facility_id  = fac.facility_id

left join {{ ref('dim_date') }} as d
on f.encounter_date = d.date_day

group by f.facility_id,fac.facility_name,d.year,d.month
order by d.year, d.month,fac.facility_name



