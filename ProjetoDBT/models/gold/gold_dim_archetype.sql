-- gold_dim_archetype.sql
-- Camada GOLD: Dimensão de Arquétipos
-- Fornece ID e métricas para cada arquétipo

WITH archetype_data AS (
    SELECT 
        archetype,
        COUNT(DISTINCT card_id) as unique_cards_count,
        SUM(min_market_price) as min_deck_core_cost,
        SUM(avg_market_price) as avg_deck_core_cost,
        MAX(max_market_price) as most_expensive_card_price,
        ROW_NUMBER() OVER(ORDER BY archetype) as archetype_id
    FROM {{ ref('gold_dim_cards') }}
    WHERE archetype IS NOT NULL
    GROUP BY 1
)

SELECT 
    archetype_id,
    archetype,
    unique_cards_count,
    min_deck_core_cost,
    avg_deck_core_cost,
    most_expensive_card_price,
    CURRENT_TIMESTAMP as created_at
FROM archetype_data
ORDER BY archetype
