{{
    config(
    materialized="table"
    )
 }}
select
    vendor_name,
    coalesce(rate_code_name, 'Group ride') as rate_code_name,
    pulocationid,
    dolocationid,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    coalesce(trip_type_name, 'По предварительному заказу') as trip_type_name,
    payment_type_name,
    total_amount
from
    {{ ref("int_green_taxi_2014__fct_trips") }} as t
left join {{ ref('payment_type') }} as p
    on t.payment_type = p.payment_type_id
left join {{ ref('vendor') }} as v
    on t.vendorid = v.vendor_id
left join {{ ref('rate_code') }} as r
    on t.ratecodeid = r.rate_code_id
left join {{ ref("trip_type") }} as tt
    on t.trip_type = tt.trip_type_id