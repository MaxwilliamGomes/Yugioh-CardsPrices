-- staging/stg_card_prices.sql
-- Carrega dados brutos da tabela de preços

select
    id,
    card_id,
    marketplace,
    price,
    currency
from {{ source('yugioh', 'card_prices') }}
