# Yu-Gi-Oh DW - DBT Documentation

## 📚 Documentação Gerada

Esta documentação foi gerada automaticamente pelo dbt e fornece uma visão completa de todas as tabelas, colunas, relacionamentos e fluxo de dados.

### 🚀 Como Acessar

#### Opção 1: Servidor Local (Recomendado)
```bash
cd ProjetoDBT
dbt docs serve
```
Acesse em: **http://localhost:8000**

#### Opção 2: Arquivos Estáticos
Os arquivos HTML estão em:
```
target/
├── manifest.json       # Metadados do projeto
├── catalog.json        # Informações de colunas
├── index.html         # Página principal
└── graphs/            # Visualizações
```

---

## 📖 O Que Você Encontra

### 1. **Documentation** (Documentação)
- Descrição de cada modelo
- Definições de colunas
- Problemas de negócio resolvidos
- Exemplos de uso

### 2. **Lineage** (Fluxo de Dados)
```
sources (raw) 
    → staging (bronze)
    → marts (silver) 
    → gold (analytics)
```
Visualize como os dados fluem através do sistema.

### 3. **Model Details**
Para cada tabela:
- ✅ Número de linhas
- ✅ Colunas e tipos
- ✅ Testes de qualidade
- ✅ Relacionamentos (FK)
- ✅ Tags e proprietário

### 4. **Source Information**
- Tabelas originais do PostgreSQL
- Estrutura de dados brutos
- Frequência de atualização

---

## 🎯 Fluxo de Dados Visual

```
┌──────────────────────────┐
│   SOURCES (Raw)          │
│  Database: yugioh        │
│  - cards                 │
│  - card_prices           │
│  - card_sets             │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  STAGING (Bronze)        │
│  Schema: public_bronze   │
│  - stg_cards             │
│  - stg_card_prices       │
│  - stg_card_sets         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  MARTS (Silver)          │
│  Schema: public_silver   │
│  - silver_cards          │
│  - silver_card_prices    │
│  - silver_card_sets      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│      GOLD (Analytics) ⭐             │
│     Schema: public_gold              │
│                                      │
│  DIMENSÕES                           │
│  - gold_dim_cards        (420)       │
│  - gold_dim_archetype    (10)        │
│                                      │
│  FATOS                               │
│  - gold_market_arbitrage (418)       │
│  - gold_rarity_premium_  (246)       │
│    analysis                          │
└──────────────────────────────────────┘
```

---

## 📊 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| **Total de Modelos** | 10 |
| **Total de Testes** | 28 |
| **Fontes** | 3 |
| **Macros** | 464 |
| **Tempo de Execução** | ~1.5s |

### Detalhes por Camada

| Camada | Modelos | Linhas | Schema |
|--------|---------|--------|--------|
| Staging (Bronze) | 3 | 420-2,173 | `public_bronze` |
| Marts (Silver) | 3 | 420-2,173 | `public_silver` |
| Gold (Analytics) | 4 | 10-418 | `public_gold` |

---

## 🔍 Explorando a Documentação

### Para Iniciantes
1. Confira o **Overview** em [docs/overview.md](overview.md)
2. Clique em uma tabela Gold para entender o problema que resolve
3. Veja os relacionamentos no **Lineage**

### Para Analistas
1. Vá para a tabela que precisa
2. Leia a descrição das colunas
3. Use os exemplos SQL fornecidos
4. Consulte os testes de qualidade

### Para Engenheiros
1. Revise o **Lineage** completo
2. Confira os **Tests** (testes de qualidade)
3. Analise os relacionamentos (FK)
4. Veja os **Compiled SQL** em `target/compiled/`

---

## 🧪 Testes de Qualidade

Todos os modelos possuem testes automáticos. Para executar:

```bash
dbt test
```

**Tipos de testes implementados:**
- ✅ **Unique** - Valores únicos (PKs)
- ✅ **Not Null** - Campos obrigatórios
- ✅ **Relationships** - Foreign Keys
- ✅ **Accepted Values** - Valores válidos

---

## 📝 Documentação de Colunas Chave

### Chaves Primárias (PK)
```
gold_dim_cards.card_id
gold_dim_archetype.archetype_id
```

### Chaves Estrangeiras (FK)
```
gold_market_arbitrage.card_id → gold_dim_cards.card_id
gold_market_arbitrage.archetype_id → gold_dim_archetype.archetype_id
gold_rarity_premium_analysis.card_id → gold_dim_cards.card_id
gold_rarity_premium_analysis.archetype_id → gold_dim_archetype.archetype_id
```

---

## 💡 Exemplos de Queries

### Exemplo 1: Buscar card com preço mais barato
```sql
SELECT 
  card_name, 
  min_market_price, 
  avg_market_price 
FROM gold_dim_cards
WHERE min_market_price < 5.00
ORDER BY min_market_price DESC
LIMIT 10
```

### Exemplo 2: Arquétipos mais baratos
```sql
SELECT 
  a.archetype,
  a.min_deck_core_cost,
  a.avg_deck_core_cost,
  a.unique_cards_count
FROM gold_dim_archetype a
ORDER BY a.min_deck_core_cost ASC
LIMIT 5
```

### Exemplo 3: Oportunidades de economia
```sql
SELECT 
  c.card_name,
  m.marketplace,
  m.current_price,
  m.overpay_amount
FROM gold_market_arbitrage m
JOIN gold_dim_cards c ON m.card_id = c.card_id
WHERE m.overpay_amount > 1.00
ORDER BY m.overpay_amount DESC
LIMIT 20
```

---

## 🔄 Regenerar Documentação

Se fizer alterações nos modelos ou schema.yml:

```bash
# Gerar novamente
dbt docs generate

# Ver em tempo real
dbt docs serve

# Ou abrir arquivo estático
start file:///C:/Users/PICHAU/Documents/yugioh/ProjetoDBT/target/index.html
```

---

## 📁 Arquivos de Documentação

```
ProjetoDBT/
├── docs/
│   ├── overview.md                    # Este arquivo
│   └── documentation_templates.md     # Templates para usar
├── models/
│   ├── schema.yml                     # Staging + Marts
│   ├── schema_gold.yml               # Dimensões + Fatos ⭐
│   ├── gold/
│   │   ├── README.md
│   │   ├── gold_dim_cards.sql
│   │   ├── gold_dim_archetype.sql
│   │   ├── gold_market_arbitrage.sql
│   │   └── gold_rarity_premium_analysis.sql
│   ├── marts/
│   └── staging/
├── target/
│   ├── manifest.json                 # Metadados (gerado)
│   ├── catalog.json                  # Catálogo (gerado)
│   └── index.html                    # Site docs (gerado)
└── dbt_project.yml
```

---

## ⚠️ Importante

- A documentação é **gerada automaticamente** a partir do código SQL e schema.yml
- Atualizações no código precisam de `dbt docs generate` para refletir
- O servidor local (`dbt docs serve`) é **apenas para desenvolvimento**
- Para produção, usar os arquivos estáticos em `target/`

---

## 🆘 Troubleshooting

### Documentação não apareça
```bash
# Limpar e regenerar tudo
dbt clean
dbt docs generate
dbt docs serve
```

### Testes falhando
```bash
# Ver detalhes dos testes
dbt test --debug

# Testar apenas um modelo
dbt test --select gold_dim_cards
```

### Servidor não inicia
```bash
# Verificar porta 8000
netstat -ano | findstr :8000

# Usar porta diferente
dbt docs serve --port 8001
```

---

**Documentação Gerada em:** 26/03/2026  
**Versão do dbt:** 1.11.2  
**Schema Version:** 2.0
