-- gold_market_arbitrage.sql
-- Camada GOLD: Análise de Oportunidades de Arbitragem
-- 🎯 Problema de Negócio: "Existe algum marketplace onde a carta está muito mais barata? 
--    Onde eu economizo mais dinheiro na compra individual?"

WITH market_diffs AS (
    SELECT 
        card_id,
        marketplace,
        price_usd,
        MIN(price_usd) OVER(PARTITION BY card_id) as min_price_global,
        MAX(price_usd) OVER(PARTITION BY card_id) as max_price_global
    FROM {{ ref('silver_card_prices') }}
    WHERE price_quality_flag = 'VALID'
)

SELECT 
    m.card_id,
    a.archetype_id,
    m.marketplace,
    m.price_usd as current_price,
    m.min_price_global,
    (m.price_usd - m.min_price_global) as overpay_amount,
    ROUND(((m.max_price_global - m.min_price_global) / NULLIF(m.max_price_global, 0)) * 100, 2) as market_spread_pct,
    CURRENT_TIMESTAMP as analyzed_at
FROM market_diffs m
JOIN {{ ref('silver_cards') }} c ON m.card_id = c.card_id
LEFT JOIN {{ ref('gold_dim_archetype') }} a ON c.archetype = a.archetype
WHERE m.price_usd = m.max_price_global -- Mostra as oportunidades de economia
ORDER BY market_spread_pct DESC
