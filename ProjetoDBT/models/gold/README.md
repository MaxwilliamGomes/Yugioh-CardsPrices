# Camada GOLD - Yu-Gi-Oh Data Warehouse

Tabelas de agregação e análise para suporte aos principais cenários de negócio dos collectors de Yu-Gi-Oh.

## 📊 Tabelas Gold

### 1. `gold_dim_cards` 🎴
**Problema de Negócio:**
"Preciso de uma visão única da carta que combine seus atributos de jogo (ATK, DEF, Imagem) com o preço atual de mercado para decidir o que comprar."

**Principais Colunas:**
- `card_id`, `card_name`, `archetype` - Dados da carta
- `attack_points`, `defense_points`, `monster_level` - Atributos de jogo
- `min_market_price`, `avg_market_price`, `max_market_price` - Preços agregados
- `total_printings`, `available_rarities` - Disponibilidade
- `price_bracket` - Categorização de valor (Budget/Mid-Range/High-End)

**Uso:** Dashboard de catálogo de cartas, análise de valor, recomendações de compra

---

### 2. `gold_archetype_costs` 💰
**Problema de Negócio:**
"Qual arquétipo é mais barato para montar hoje? Qual o investimento mínimo e máximo para cada estratégia?"

**Principais Colunas:**
- `archetype` - Estratégia/tema da carta
- `unique_cards_count` - Quantidade de cartas únicas do arquétipo
- `min_deck_core_cost` - Investimento mínimo para montar
- `avg_deck_core_cost` - Investimento médio
- `most_expensive_card_price` - Carta mais cara do arquétipo

**Uso:** Planejamento de orçamento, comparação de decks, índices de viabilidade

---

### 3. `gold_market_arbitrage` 🏪
**Problema de Negócio:**
"Existe algum marketplace onde a carta está muito mais barata? Onde eu economizo mais dinheiro na compra individual?"

**Principais Colunas:**
- `card_name`, `marketplace` - Identifica a oportunidade
- `current_price`, `min_price_global` - Comparação de preços
- `overpay_amount` - Economia potencial
- `market_spread_pct` - Volatilidade de preços

**Uso:** Otimização de compras, monitoramento de marketplaces, alertas de oportunidades

---

### 4. `gold_rarity_premium_analysis` ✨
**Problema de Negócio:**
"Vale a pena pagar pela raridade? Quanto eu pago a mais por uma carta 'Secret Rare' em comparação à sua versão mais simples?"

**Principais Colunas:**
- `card_name`, `set_rarity` - Identifica a versão
- `rarity_price`, `base_price` - Comparação monetária
- `luxury_multiplier` - Quanto custa a mais em proporção
- `rarity_premium_usd` - Preço absoluto a mais

**Uso:** Análise de valor de coleção, decisão de upgrade de raridade

---

## 🔄 Fluxo de Dados

```
Silver Tables (staging/marts)
├── silver_cards
├── silver_card_prices
└── silver_card_sets
    ↓
Gold Tables (analytics)
├── gold_dim_cards (base para todas)
├── gold_archetype_costs
├── gold_market_arbitrage
└── gold_rarity_premium_analysis
```

## 📋 Dicionário de Qualidade

Todas as tabelas respeitam as flags de qualidade existentes:
- `price_quality_flag = 'VALID'` - Preços validados
- `data_quality_flag = 'VALID'` - Dados de sets/raridade validados

---

**Última Atualização:** {{ run_started_at }}
