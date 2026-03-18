{{ config(
    materialized='incremental',
    alias='astros',
    engine='MergeTree()',
) }}

SELECT
    '{}' AS json_data,           -- placeholder column
    now() AS insert_datetime
WHERE 1=0  