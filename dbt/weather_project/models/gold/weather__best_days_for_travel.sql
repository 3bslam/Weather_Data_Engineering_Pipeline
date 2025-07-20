{{ config(materialized='view') }}

with weather as (
    select
        l.city,
        date(w.time) as day,
        w.temperature_c,
        w.humidity,
        w.wind_kph
    from {{ ref('stg_weather_data') }} w
    join {{ ref('stg_locations') }} l
        on w.location_id = l.location_id
    where lower(l.country) = 'egypt'
      and date(w.time) = current_date
),

classified_weather as (
    select
        city,
        day,
        temperature_c,
        humidity,
        wind_kph,
        case
            when temperature_c between 22 and 28 and humidity between 30 and 55 and wind_kph < 15 then 'Excellent'
            when temperature_c between 20 and 30 and humidity between 25 and 65 and wind_kph < 20 then 'Good'
            when temperature_c between 18 and 32 and humidity between 20 and 70 and wind_kph < 25 then 'Fair'
            else 'Bad'
        end as weather_quality
    from weather
)

select
    city,
    day,
    weather_quality,
    count(*) as hours_count
from classified_weather
group by city, day, weather_quality
order by weather_quality, hours_count desc
