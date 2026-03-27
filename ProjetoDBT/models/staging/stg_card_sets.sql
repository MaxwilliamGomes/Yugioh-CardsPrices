-- staging/stg_card_sets.sql
-- Carrega dados brutos da tabela de sets

select
    id,
    card_id,
    set_name,
    set_code,
    set_rarity,
    set_price
from {{ source('yugioh', 'card_sets') }}
