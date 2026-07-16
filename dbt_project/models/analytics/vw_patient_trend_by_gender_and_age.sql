    
with patient as(
    select
        f.patient_id,
        p.gender,
        case 
            when p.age < 18 then '<18'
            when p.age between 18 and 34 then '18-34'
            when p.age between 35 and 49 then '35-49'
            when p.age between 50 and 64 then '50-64'
            else '65+'
        end as age_group,
        d.year,
        d.month
    from {{ ref('fact_encounter') }} as f
    
    left join {{ ref('dim_patient') }} as p
    on f.patient_id = p.patient_id
    left join {{ ref('dim_date') }} as d
    on f.encounter_date = d.date_day 
    where f.encounter_date >= '2010-01-01'
)

select 
    year,
    month,
    gender,
    age_group,
    count(distinct patient_id) as unique_patients,
    count(*) as encounter_count
from patient
group by year,month,gender,age_group
order by year desc,month desc,gender,age_group
