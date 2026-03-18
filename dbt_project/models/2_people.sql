{{ config(
    materialized='materialized_view',
    alias='people',
    engine='ReplacingMergeTree()',
    order_by='(craft, name)'
) }}

SELECT
    JSONExtractString(person, 'craft') AS craft,
    JSONExtractString(person, 'name') AS name,
    now() AS _inserted_at
FROM astros_raw
ARRAY JOIN JSONExtractArrayRaw(json_data, 'people') AS person