# 🎮 DBT Setup - Yu-Gi-Oh DW

## ✅ Instalação Concluída!

dbt core foi instalado e configurado com sucesso para sua pipeline Yu-Gi-Oh.

### 📦 O que foi instalado
- ✅ `dbt-core==1.11.2`
- ✅ `dbt-postgres==1.10.0`

---

## 🏗️ Estrutura do Projeto

```
yugioh/
├── dbt_project.yml                 # Configuração principal do dbt
├── models/
│   ├── schema.yml                  # Definição das SOURCES
│   ├── staging/                    # Camada BRONZE (referências às tabelas raw)
│   │   ├── stg_cards.sql
│   │   ├── stg_card_prices.sql
│   │   └── stg_card_sets.sql
│   └── marts/                      # Camada SILVER (transformações)
│       ├── silver_cards.sql
│       ├── silver_card_prices.sql
│       └── silver_card_sets.sql
├── target/                         # Output do dbt (SQL compilado)
└── logs/                           # Logs de execução
```

---

## 📊 Camadas Criadas

### 🟤 BRONZE (Staging - staging/)
Referências às tabelas raw do banco:
- `stg_cards` → carga bruta de cards
- `stg_card_prices` → carga bruta de preços
- `stg_card_sets` → carga bruta de sets

### 🟢 SILVER (Marts - marts/)
Transformações e limpeza de dados:
- `silver_cards` - Cards com validações e normalizações
- `silver_card_prices` - Preços com validação e conversão de moedas
- `silver_card_sets` - Sets com tratamento de valores inválidos

---

## 🚀 Comandos Principais

### Rodar todos os modelos
```bash
dbt run
```

### Rodar apenas modelos SILVER
```bash
dbt run -s tag:silver
```

### Testar qualidade dos dados
```bash
dbt test
```

### Gerar documentação
```bash
dbt docs generate
dbt docs serve  # Abre no navegador
```

### Verificar dependências
```bash
dbt run --select +silver_cards+
```

### Ver as SQL compiladas
```bash
dbt compile
```

---

## 📋 Transformações SILVER

### 1️⃣ `silver_cards`
**Limpeza de dados de cards:**
- Trim em campos de texto
- Validação de ATK/DEF (remove negativos)
- Validação de LEVEL (1-13)
- Normalização de attribute (`NaN` → `UNKNOWN`)
- Remove registros incomplete

📊 Resultado: **420 cards limpos**

### 2️⃣ `silver_card_prices`
**Tratamento de preços:**
- Validação de valores (> 0)
- Conversão de EUR para USD (taxa: 1.10)
- Arredonda para 2 casas decimais
- Flag de qualidade de dados
- Remove preços inválidos

📊 Resultado: **1.591 preços validados**

### 3️⃣ `silver_card_sets`
**Normalização de sets:**
- Padronização de set_rarity
- Validação de preços
- Flag de qualidade (VALID/INCOMPLETE/INVALID)
- Remove registros sem card_id

📊 Resultado: **2.173 registros de sets**

---

## 🔄 Fluxo de Dados

```
RAW (public schema)
  ├── cards (420)
  ├── card_prices (1.591)
  └── card_sets (2.173)
         ↓ dbt
    BRONZE (schema: bronze)
      ├── stg_cards
      ├── stg_card_prices
      └── stg_card_sets
         ↓ dbt
    SILVER (schema: silver)
      ├── silver_cards ✅ Tratado
      ├── silver_card_prices ✅ Tratado
      └── silver_card_sets ✅ Tratado
```

---

## 🔧 Próximos Passos

1. **Adicionar Testes dbt**
   ```bash
   mkdir tests/silver
   # Criar teste de integridade referencial, valores nulos, etc
   ```

2. **Criar Camada GOLD**
   ```bash
   mkdir models/gold
   # Agregações e mart analytics final
   ```

3. **Configurar Documentação**
   ```bash
   dbt docs generate
   dbt docs serve
   ```

4. **Implementar alertas de qualidade**
   - Monitorar timestamp de carregamento
   - Alertar se número de registros cair demais
   - Validar freshness dos dados

---

## 🐛 Troubleshooting

### Erro: "Profile 'yugioh_dw' not found"
```
Verifique: C:\Users\PICHAU\.dbt\profiles.yml
```

### Erro: "Connection refused"
```bash
# Certificar que PostgreSQL está rodando
docker ps | grep postgres
docker-compose up -d
```

### Limpar artifacts (target/)
```bash
dbt clean
```

---

## 📚 Recursos

- [Documentação dbt](https://docs.getdbt.com)
- [dbt-postgres](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup)
- [Best Practices](https://docs.getdbt.com/guides/best-practices)

---

**Data de Setup:** 2026-03-26  
**Versão dbt:** 1.11.2  
**Postgres Adapter:** 1.10.0
