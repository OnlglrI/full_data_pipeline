{{
    config(
        materialized="table"
    )
 }}

select
    pulocationid,
    dolocationid,
    count(*) as trip_count,
    avg(total_amount) as avg_total_amount
from
    {{ ref('int_green_taxi_2014__fct_trips') }}
group by 1, 2
order by trip_count desc