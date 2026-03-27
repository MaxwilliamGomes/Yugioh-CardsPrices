-- gold_dim_cards.sql
-- Camada GOLD: Dimensão de Cards
-- 🎯 Problema de Negócio: "Preciso de uma visão única da carta que combine seus atributos de jogo 
--    (ATK, DEF, Imagem) com o preço atual de mercado para decidir o que comprar."

WITH current_prices AS (
    SELECT 
        card_id,
        MIN(price_usd) as min_market_price,
        AVG(price_usd) as avg_market_price,
        MAX(price_usd) as max_market_price
    FROM {{ ref('silver_card_prices') }}
    WHERE price_quality_flag = 'VALID'
    GROUP BY 1
),

set_metrics AS (
    SELECT 
        card_id,
        COUNT(DISTINCT set_id) as total_printings,
        STRING_AGG(DISTINCT set_rarity, ', ') as available_rarities
    FROM {{ ref('silver_card_sets') }}
    WHERE data_quality_flag = 'VALID'
    GROUP BY 1
)

SELECT 
    c.card_id,
    c.card_name,
    c.archetype,
    c.card_type,
    c.monster_attribute,
    c.monster_race,
    c.monster_level,
    c.attack_points,
    c.defense_points,
    c.image_url,
    p.min_market_price,
    p.avg_market_price,
    p.max_market_price,
    s.total_printings,
    s.available_rarities,
    CASE 
        WHEN p.min_market_price < 2.00 THEN 'Budget (Under $2)'
        WHEN p.min_market_price BETWEEN 2.00 AND 15.00 THEN 'Mid-Range'
        ELSE 'High-End Investment'
    END as price_bracket,
    CURRENT_TIMESTAMP as updated_at
FROM {{ ref('silver_cards') }} c
LEFT JOIN current_prices p ON c.card_id = p.card_id
LEFT JOIN set_metrics s ON c.card_id = s.card_id
