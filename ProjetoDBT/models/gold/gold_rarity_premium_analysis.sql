-- gold_rarity_premium_analysis.sql
-- Camada GOLD: Análise de Ágio por Raridade
-- 🎯 Problema de Negócio: "Vale a pena pagar pela raridade? 
--    Quanto eu pago a mais por uma carta 'Secret Rare' em comparação à sua versão mais simples?"

WITH rarity_prices AS (
    SELECT 
        card_id,
        set_rarity,
        AVG(set_price_amount) as avg_rarity_price
    FROM {{ ref('silver_card_sets') }}
    WHERE data_quality_flag = 'VALID'
    GROUP BY 1, 2
),

base_prices AS (
    -- Pega a raridade mais barata de cada carta
    SELECT 
        card_id,
        MIN(avg_rarity_price) as base_price
    FROM rarity_prices
    GROUP BY 1
)

SELECT 
    r.card_id,
    a.archetype_id,
    r.set_rarity,
    r.avg_rarity_price as rarity_price,
    b.base_price,
    ROUND((r.avg_rarity_price / NULLIF(b.base_price, 0)), 2) as luxury_multiplier,
    (r.avg_rarity_price - b.base_price) as rarity_premium_usd,
    CURRENT_TIMESTAMP as analyzed_at
FROM rarity_prices r
JOIN base_prices b ON r.card_id = b.card_id
JOIN {{ ref('silver_cards') }} c ON r.card_id = c.card_id
LEFT JOIN {{ ref('gold_dim_archetype') }} a ON c.archetype = a.archetype
WHERE r.avg_rarity_price > b.base_price -- Foca apenas em versões que possuem 'ágio'
ORDER BY luxury_multiplier DESC
