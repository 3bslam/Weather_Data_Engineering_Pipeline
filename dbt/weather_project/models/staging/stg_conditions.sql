{{ config(materialized='view') }}

select
    id as condition_id,
    description,
    icon_url,
    code
from {{ source('weather', 'conditions') }}
