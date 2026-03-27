# 🎮 Camada SILVER - Yu-Gi-Oh DW

A camada SILVER contém modelos dbt que transformam e tratam os dados das tabelas BRONZE (raw).

## 📊 Modelos Silver

### 1. `silver_cards.sql`
**Transformação de dados de cards**

✅ Operações de limpeza:
- Trim em campos de texto (name, type, race, attribute, archetype)
- Validação de ATK/DEF (remove valores negativos ou nulos)
- Validação de LEVEL (aceita apenas 1-13)
- Normalização de attribute (converte valores inválidos para 'UNKNOWN')
- Remove registros sem card_id, name ou type

📦 Output: Tabela `silver_cards`

---

### 2. `silver_card_prices.sql`
**Transformação e tratamento de preços**

✅ Operações de limpeza:
- Validação de preços (remove valores ≤ 0)
- Conversão de moedas para USD (EUR * 1.10)
- Arredondamento de valores para 2 casas decimais
- Normalização de currency (EUR, USD, OTHER)
- Flag de qualidade de dados (VALID/INVALID)
- Remove registros sem card_id

📦 Output: Tabela `silver_card_prices`

---

### 3. `silver_card_sets.sql`
**Transformação de dados de sets**

✅ Operações de limpeza:
- Trim em campos de texto (set_name, set_code)
- Normalização de set_rarity (valores nulos → 'UNKNOWN')
- Validação de set_price (remove valores ≤ 0)
- Flag de qualidade de dados (VALID/INCOMPLETE/INVALID)
- Remove registros sem card_id

📦 Output: Tabela `silver_card_sets`

---

## 🚀 Como usar

### Executar todos os modelos:
```bash
dbt run
```

### Executar apenas models silver:
```bash
dbt run -s tag:silver
```

### Fazer testes de qualidade:
```bash
dbt test
```

### Gerar documentação:
```bash
dbt docs generate
```

### Ver dependências:
```bash
dbt run --select +silver_cards+
```

---

## 🔄 Estrutura de Dados

```
BRONZE (Raw)          SILVER (Tratado)
├── cards      →      silver_cards
├── card_prices  →    silver_card_prices  
└── card_sets   →     silver_card_sets
```

---

## 📝 Convenções

- ✅ Todas as transformações usam CTE (With)
- ✅ Nomeação clara: `silver_<tabela_original>`
- ✅ Timestamps: `loaded_at` para rastrear quando foi carregado
- ✅ Flags de qualidade para validar dados
- ✅ Comentários em SQL explicando cada transformação

---

## 🔗 Próximos passos

1. Adicionar testes dbt (tests/silver/)
2. Criar modelos GOLD com agregações finais
3. Configurar alertas para qualidade de dados
4. Implementar SLAs e data freshness
