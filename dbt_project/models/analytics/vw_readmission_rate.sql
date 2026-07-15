with encounter_orders as(
    select 
        encounter_id,
        patient_id,
        encounter_date,
        facility_id,
        lag(encounter_date) over(
            partition by patient_id,facility_id
            order by encounter_date
        ) as previous_encounter_date
    from {{ ref("fact_encounter") }}
    where encounter_date >= '2010-01-01' and encounter_class = 'inpatient'
),

flaged as(
    select
        *,
        case
            when previous_encounter_date is not null and
                (encounter_date - previous_encounter_date ) <= 30
            then
                true
            else
                false
        end as is_readmission
    from encounter_orders     

),

final as (
    select
        f.facility_id,
        d.year,
        fac.facility_name,
        count (*) as total_encounters,
        sum(case when f.is_readmission then 1 else 0 end ) as readmission_count,
        round(
            100.0 * sum(case when f.is_readmission then 1 else 0 end ) / count(*),
            1
        )as readmission_rate_pct
    from flaged as f
    left join {{ ref("dim_facility") }} as fac
    on f.facility_id = fac.facility_id

    left join {{ ref("dim_date") }} as d
    on f.encounter_date = d.date_day

    group by f.facility_id,d.year,fac.facility_name
    having count(*) >= 5
    order by d.year,f.facility_id
)

select * from final
