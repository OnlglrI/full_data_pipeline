{{
    config(
    materialized="table"
    )
}}
select
    trip_date,
    vendor_name,
    trip_count,
    avg_distance,
    avg_total,
    avg_tip
from {{ ref('int_green_taxi_2014__fct_trip_stats') }} as dmts
left join {{ ref('vendor') }} as v
    on dmts.vendorid = v.vendor_id
