-- marts/silver_card_prices.sql
-- Camada de transformação SILVER para preços
-- Tratamento, validação e conversão de moedas

with stg_card_prices as (
    select * from {{ ref('stg_card_prices') }}
),

price_validation as (
    select
        id as price_id,
        card_id,
        trim(marketplace) as marketplace,
        -- Validação de preço
        case
            when price is null or price <= 0 then null
            else round(price::numeric, 2)
        end as price_amount,
        currency,
        -- Conversão para taxa padrão (USD)
        case
            when currency = 'EUR' then round((price * 1.10)::numeric, 2)
            when currency = 'USD' then round(price::numeric, 2)
            else round(price::numeric, 2)
        end as price_usd,
        case
            when currency = 'EUR' then 'EUR'
            when currency = 'USD' then 'USD'
            else 'OTHER'
        end as currency_normalized
    from stg_card_prices
    where card_id is not null
        and marketplace is not null
)

select
    price_id,
    card_id,
    marketplace,
    price_amount,
    price_usd,
    currency_normalized,
    case
        when price_usd is null then 'INVALID'
        else 'VALID'
    end as price_quality_flag,
    current_timestamp as loaded_at
from price_validation
