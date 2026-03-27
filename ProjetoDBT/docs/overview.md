# Yu-Gi-Oh Data Warehouse - Documentação

## 📊 Visão Geral do Projeto

Este é um data warehouse especializado em cartas de Yu-Gi-Oh, com foco em análise de preços, raridades e estratégias (arquétipos) de jogo.

**Stack Tecnológico:**
- **Data Orchestration:** dbt (Data Build Tool)
- **Database:** PostgreSQL
- **Extract/Load:** Python (src/extract_load.py)
- **Container:** Docker + Docker Compose
- **MCP Server:** Model Context Protocol para integração

---

## 🔄 Arquitetura de Fluxo de Dados

```
┌─────────────────────────────────────┐
│     SOURCES (Raw Tables)            │
│  - cards                            │
│  - card_prices                      │
│  - card_sets                        │
└──────────────────┬──────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   STAGING (BRONZE)   │
        │  - stg_cards         │
        │  - stg_card_prices   │
        │  - stg_card_sets     │
        └──────────┬───────────┘
                   │
        ┌──────────▼───────────┐
        │  MARTS (SILVER)      │
        │  (Transformação)     │
        │  - silver_cards      │
        │  - silver_card_prices│
        │  - silver_card_sets  │
        └──────────┬───────────┘
                   │
        ┌──────────▼──────────────────┐
        │   GOLD (ANALYTICS)          │
        │                             │
        │   DIMENSÕES                 │
        │  ├─ gold_dim_cards          │
        │  └─ gold_dim_archetype      │
        │                             │
        │   FATOS                     │
        │  ├─ gold_market_arbitrage   │
        │  └─ gold_rarity_premium_    │
        │      analysis               │
        └─────────────────────────────┘
```

---

## 🎯 Camadas do Data Warehouse

### 1️⃣ STAGING (Bronze)
**Schema:** `public_bronze`  
**Propósito:** Limpeza mínima e estruturação dos dados brutos

| Tabela | Linhas | Descrição |
|--------|--------|-----------|
| `stg_cards` | 420 | Cards com validação de tipos e valores |
| `stg_card_prices` | 1,591 | Preços estruturados com marketplace |
| `stg_card_sets` | 2,173 | Sets com raridade e preços |

**Transformações Aplicadas:**
- ✅ Trim em strings
- ✅ Validação de tipos
- ✅ Remoção de duplicatas

---

### 2️⃣ MARTS (Silver)
**Schema:** `public_silver`  
**Propósito:** Transformações de negócio com validações e tratamentos

| Tabela | Linhas | Descrição |
|--------|--------|-----------|
| `silver_cards` | 420 | Cards com tratamento de valores nulos, validação de ATK/DEF/LEVEL |
| `silver_card_prices` | 1,591 | Preços com flags de qualidade (VALID/INVALID) |
| `silver_card_sets` | 2,173 | Sets com flags de qualidade e normalização |

**Transformações Aplicadas:**
- ✅ Validação de ATK/DEF (rejeita valores negativos)
- ✅ Validação de LEVEL (1-13)
- ✅ Padronização de ATTRIBUTE (NaN → UNKNOWN)
- ✅ Flag de qualidade de dados

---

### 3️⃣ GOLD (Analytics) ⭐
**Schema:** `public_gold`  
**Propósito:** Análises prontas para decisões de negócio

#### **DIMENSÕES**

##### `gold_dim_cards` (420 linhas)
Dimensão consolidada com todos os atributos do card + preços de mercado
- **Chave Primária:** `card_id`
- **Granularidade:** 1 linha por card
- **Uso:** Base para todas as análises

**Colunas Principais:**
```sql
card_id, card_name, archetype, card_type,
monster_attribute, monster_race, monster_level,
attack_points, defense_points, image_url,
min_market_price, avg_market_price, max_market_price,
total_printings, available_rarities, price_bracket
```

---

##### `gold_dim_archetype` (10 linhas)
Dimensão de estratégias/arquétipos com métricas de custo
- **Chave Primária:** `archetype_id`
- **Chave Negócio:** `archetype`
- **Granularidade:** 1 linha por arquétipo único

**Colunas Principais:**
```sql
archetype_id, archetype,
unique_cards_count,
min_deck_core_cost,
avg_deck_core_cost,
most_expensive_card_price
```

---

#### **FATOS**

##### `gold_market_arbitrage` (418 linhas)
Fato de oportunidades de economia entre marketplaces
- **Granularidade:** 1 linha por (card, marketplace)
- **Relacionamentos:**
  - FK: `card_id` → `gold_dim_cards.card_id`
  - FK: `archetype_id` → `gold_dim_archetype.archetype_id`

**Problema Resolvido:** 
"Existe algum marketplace onde a carta está mais barata? Onde economizo?"

**Colunas Principais:**
```sql
card_id, archetype_id, marketplace,
current_price, min_price_global,
overpay_amount, market_spread_pct
```

---

##### `gold_rarity_premium_analysis` (246 linhas)
Fato de análise de ágio por raridade
- **Granularidade:** 1 linha por (card, set_rarity) onde há ágio
- **Relacionamentos:**
  - FK: `card_id` → `gold_dim_cards.card_id`
  - FK: `archetype_id` → `gold_dim_archetype.archetype_id`

**Problema Resolvido:** 
"Vale a pena pagar pela raridade? Quanto sai mais caro?"

**Colunas Principais:**
```sql
card_id, archetype_id, set_rarity,
rarity_price, base_price,
luxury_multiplier, rarity_premium_usd
```

---

## 📊 Modelo de Dados (Star Schema)

```
                    gold_dim_cards
                          │
                    ┌─────┴─────┐
                    │           │
            gold_dim_archetype   │
                    │ ◄─────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
    gold_market_arbitrage   gold_rarity_premium_analysis
```

**Padrão:** Star Schema (Schema em Estrela)
- Dimensões centralizadas → sem redundância
- Fatos normalizados → apenas IDs + métricas
- Relacionamentos FK garantem integridade

---

## 🚀 Como Usar os Dados

### Exemplo 1: Qual é o preço de um card?
```sql
SELECT 
  card_name, 
  min_market_price, 
  avg_market_price, 
  price_bracket
FROM gold_dim_cards
WHERE card_name = 'Blue-Eyes White Dragon'
```

### Exemplo 2: Qual arquétipo é mais barato para montar?
```sql
SELECT 
  archetype,
  unique_cards_count,
  min_deck_core_cost,
  avg_deck_core_cost
FROM gold_dim_archetype
ORDER BY min_deck_core_cost
LIMIT 5
```

### Exemplo 3: Onde compro mais barato cada card?
```sql
SELECT 
  c.card_name,
  m.marketplace,
  m.current_price,
  m.overpay_amount
FROM gold_market_arbitrage m
JOIN gold_dim_cards c ON m.card_id = c.card_id
WHERE m.overpay_amount > 0
ORDER BY m.overpay_amount DESC
```

### Exemplo 4: Qual raridade vale mais a pena?
```sql
SELECT 
  card_name,
  set_rarity,
  rarity_price,
  base_price,
  luxury_multiplier
FROM gold_rarity_premium_analysis
WHERE luxury_multiplier > 2.0  -- Custa 2x ou mais
ORDER BY rarity_premium_usd DESC
```

---

## 📈 Qualidade de Dados

### Validações Implementadas

**Staging (Bronze):**
- ✅ Trim de espaços em branco
- ✅ Normalização de tipos

**Marts (Silver):**
- ✅ `price_quality_flag` - Indica preços válidos
- ✅ `data_quality_flag` - Indica dados de set válidos
- ✅ Validação de ATK/DEF (rejeita negativos)
- ✅ Validação de LEVEL (1-13)

**Gold:**
- ✅ Foreign Keys garantem relacionalidade
- ✅ Testes de unicidade em chaves primárias
- ✅ NOT NULL em campos críticos

---

## 🔧 Executar o Pipeline

```bash
# Entrar no diretório do projeto
cd ProjetoDBT

# Executar todos os modelos
dbt run

# Executar testes de qualidade
dbt test

# Gerar documentação
dbt docs generate
dbt docs serve  # Abre em http://localhost:8000

# Rodar um modelo específico
dbt run --select gold_dim_cards
```

---

## 📝 Dicionário de Termos

| Termo | Definição |
|-------|-----------|
| **Archetype** | Estratégia/tema de carta (ex: Dragon, Zombie, Synchro) |
| **Set** | Coleção de cartas lançada (ex: Blue Eyes Chaos Max) |
| **Rarity** | Raridade da carta em um set (Common, Super Rare, Secret Rare) |
| **Marketplace** | Plataforma de venda (TCGPlayer, Cardmarket, etc) |
| **Price Bracket** | Categorização de valor (Budget <$2, Mid-Range, High-End) |
| **Luxury Multiplier** | Quanto custa a raridade em proporção à versão base |

---

## 📞 Suporte

Para dúvidas sobre o modelo ou dados:
- Verifique a documentação gerada: `dbt docs serve`
- Consulte os comentários nos arquivos SQL
- Revise o arquivo [README.md](../README.md)

---

**Última Atualização:** 26/03/2026  
**Versão:** 1.0.0  
**Status:** ✅ Produção
