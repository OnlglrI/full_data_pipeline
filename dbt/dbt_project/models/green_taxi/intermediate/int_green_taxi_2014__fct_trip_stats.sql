{{
    config(
    materialized="table"
    )
}}
select
    lpep_pickup_datetime::date as trip_date,
    vendorid,
    count(*) as trip_count,
    avg(trip_distance) as avg_distance,
    avg(total_amount) as avg_total,
    avg(tip_amount) as avg_tip
from {{ ref('staging_green_taxi_2014') }}
group by 1, 2
