select
    f.facility_id,
    fac.facility_name,
    d.year,
    d.month,
    round(avg(f.length_of_stay_hours), 1) as avg_length_of_stay_hours,
    count(*) as encounter_count

from {{ ref('fact_encounter') }} as f
left join {{ ref('dim_facility') }} as fac
    on f.facility_id = fac.facility_id
left join {{ ref('dim_date') }} as d
    on f.encounter_date = d.date_day

where f.length_of_stay_hours is not null

group by f.facility_id, fac.facility_name, d.year, d.month
order by d.year, d.month, fac.facility_name