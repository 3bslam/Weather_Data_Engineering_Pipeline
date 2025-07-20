{{ config(materialized='view') }}

select
    id as location_id,
    city,
    region,
    country,
    lat,
    lon,
    tz_id,
    local_time
from {{ source('weather', 'locations') }}
where lower(country) = 'egypt'

