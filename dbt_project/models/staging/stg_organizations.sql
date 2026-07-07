SELECT
    "Id" as organizations_id,
    "NAME" as organizations_name,
    "CITY" as city,
    "STATE" as state,
    cast("REVENUE" as numeric) as revenue,
    cast("UTILIZATION" as numeric) as utilization
FROM{{ source("raw","raw_organizations") }}