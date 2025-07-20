{{ config(materialized='table') }}

with weather as (
    select *
    from {{ ref('stg_weather_data') }}
),

locations as (
    select *
    from {{ ref('stg_locations') }}
),

conditions as (
    select *
    from {{ ref('stg_conditions') }}
),

joined as (
    select
        w.weather_data_id,
        l.city,
        l.country,
        w.time::date as date,
        c.description as weather_condition,
        w.temperature_c,
        w.feelslike_c,
        w.humidity,
        w.wind_kph,
        w.gust_kph,
        w.pressure_mb,
        w.uv_index
    from weather w
    join locations l on w.location_id = l.location_id
    join conditions c on w.condition_id = c.condition_id
)

select
    city,
    country,
    date,
    round(avg(temperature_c)::numeric, 1) as avg_temp_c,
    round(avg(feelslike_c)::numeric, 1) as avg_feelslike,
    round(avg(humidity)::numeric, 1) as avg_humidity,
    round(avg(wind_kph)::numeric, 1) as avg_wind,
    max(weather_condition) as dominant_condition
from joined
group by city, country, date
order by date desc
