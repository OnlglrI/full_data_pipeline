{{
    config(
    materialized="table"
    )
 }}

select
    "VendorID" AS vendorid,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    store_and_fwd_flag,
    "RatecodeID" as ratecodeid,
    greatest(coalesce("PULocationID",0), 0) AS pulocationid,
    greatest(coalesce("DOLocationID",0), 0) AS dolocationid,
    greatest(coalesce(passenger_count,0), 0) AS passenger_count,
    greatest(coalesce(trip_distance,0), 0) AS trip_distance,
    greatest(coalesce(fare_amount,0), 0) AS fare_amount,
    greatest(coalesce(extra,0), 0) AS extra,
    greatest(coalesce(mta_tax,0), 0) AS mta_tax,
    greatest(coalesce(tip_amount,0), 0) AS tip_amount,
    greatest(coalesce(tolls_amount,0), 0) AS tolls_amount,
    ehail_fee,
    greatest(coalesce(improvement_surcharge,0), 0) AS improvement_surcharge,
    greatest(coalesce(total_amount,0), 0) AS total_amount,
    payment_type,
    greatest(coalesce(trip_type,0), 0) AS trip_type,
    congestion_surcharge
from
    {{ source("green_taxi_src", "green_tripdata_2014") }}