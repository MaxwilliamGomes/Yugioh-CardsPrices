-- staging/stg_cards.sql
-- Carrega dados brutos da tabela de cards
-- Sem transformações, apenas select dos dados

select
    id,
    name,
    type,
    atk,
    def,
    level,
    race,
    attribute,
    archetype,
    image_url
from {{ source('yugioh', 'cards') }}
