{{
    config(
    materialized="table"
    )
}}

select
    trip_date,
    vendor_name,
    payment_type_name,
    sum (gross_revenue) as sum_gross_revenue,
    sum (net_revenue) as sum_net_revenue
from {{ ref('int_green_taxi_2014__fct_revenue') }} as fct_r
left join {{ ref("vendor") }} as v
    on fct_r.vendorid = v.vendor_id
left join {{ ref("payment_type") }} as p
    on fct_r.payment_type = p.payment_type_id
group by 1,2,3