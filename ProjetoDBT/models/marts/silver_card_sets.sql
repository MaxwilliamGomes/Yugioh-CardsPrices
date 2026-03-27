-- marts/silver_card_sets.sql
-- Camada de transformação SILVER para sets
-- Tratamento e padronização de dados

with stg_card_sets as (
    select * from {{ ref('stg_card_sets') }}
)

select
    id as set_id,
    card_id,
    trim(set_name) as set_name,
    trim(set_code) as set_code,
    -- Padronização de rarity
    case
        when set_rarity is null or trim(set_rarity) = '' then 'UNKNOWN'
        else trim(set_rarity)
    end as set_rarity,
    -- Validação de preço
    case
        when set_price is null or set_price <= 0 then null
        else round(set_price::numeric, 2)
    end as set_price_amount,
    -- Flag de qualidade
    case
        when card_id is null then 'INVALID'
        when set_name is null or trim(set_name) = '' then 'INCOMPLETE'
        else 'VALID'
    end as data_quality_flag,
    current_timestamp as loaded_at
from stg_card_sets
where card_id is not null
