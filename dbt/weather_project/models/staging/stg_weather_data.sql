{{ config(materialized='view') }}

select
    id as weather_data_id,
    location_id,
    condition_id,
    temperature_c,
    wind_kph,
    humidity,
    pressure_mb,
    feelslike_c,
    uv_index,
    gust_kph,
    time,
    insert_at
from {{ source('weather', 'weather_data') }}
