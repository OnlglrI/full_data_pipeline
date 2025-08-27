{{
    config(
    materialized="table"
    )
}}

select
    lpep_pickup_datetime as trip_date,
    vendorid,
    payment_type,
    sum(fare_amount + tip_amount + tolls_amount + improvement_surcharge + mta_tax + extra) as gross_revenue,
    sum(total_amount) as net_revenue
from {{ ref('staging_green_taxi_2015') }}
group by 1, 2, 3