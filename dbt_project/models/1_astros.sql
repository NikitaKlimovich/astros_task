{{ config(
    materialized='incremental',
    alias='astros_raw',
    engine='MergeTree()',
    post_hook=[
        "ALTER TABLE {{ this }} MODIFY COLUMN _inserted_at DEFAULT now()"
    ]
) }}

SELECT
    '{}' AS json_data,           -- placeholder column
    now() AS _inserted_at
WHERE 1=0  