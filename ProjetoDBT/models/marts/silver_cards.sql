-- marts/silver_cards.sql
-- Camada de transformação SILVER para cards
-- Tratamento e limpeza de dados

with stg_cards as (
    select * from {{ ref('stg_cards') }}
)

select
    id as card_id,
    trim(name) as card_name,
    trim(type) as card_type,
    -- Validação de ATK
    case 
        when atk is null or atk < 0 then null
        else atk 
    end as attack_points,
    -- Validação de DEF
    case 
        when def is null or def < 0 then null
        else def 
    end as defense_points,
    -- Validação de LEVEL
    case 
        when level is null or level <= 0 or level > 13 then null
        else level 
    end as monster_level,
    trim(race) as monster_race,
    -- Padronização de attribute
    case
        when attribute is null or attribute = 'NaN' then 'UNKNOWN'
        else trim(attribute)
    end as monster_attribute,
    trim(archetype) as archetype,
    image_url,
    -- Metadata
    current_timestamp as loaded_at
from stg_cards
where id is not null
    and name is not null
    and type is not null
