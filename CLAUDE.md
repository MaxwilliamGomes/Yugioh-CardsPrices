# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Yu-Gi-Oh! Cards Prices — a data engineering pipeline that fetches card data from the [YGOProDeck API](https://db.ygoprodeck.com/api/v7/cardinfo.php) and transforms it through a Bronze → Silver → Gold medallion architecture using dbt and PostgreSQL.

## Common Commands

### Infrastructure
```bash
# Start PostgreSQL (port 5433)
docker-compose up -d

# Stop PostgreSQL
docker-compose down
```

### Extraction (Bronze ingestion)
```bash
# Run the extract & load script — drops and recreates raw tables each run
python src/extract_load.py
```

### dbt (Transformations)
```bash
cd ProjetoDBT

# Run all models
dbt run

# Run a single model
dbt run --select silver_card_prices

# Run by layer tag
dbt run --select tag:staging
dbt run --select tag:silver
dbt run --select tag:gold

# Run tests
dbt test

# Generate and serve docs
dbt docs generate
dbt docs serve
```

### MCP Server (optional — exposes DW to VS Code Copilot)
```bash
python src/mcp_postgres_server.py
```

## Architecture

### Data Flow
```
YGOProDeck API → src/extract_load.py → PostgreSQL (public schema)
                                              ↓
                                    dbt: staging (bronze schema)
                                              ↓
                                    dbt: marts  (silver schema)
                                              ↓
                                    dbt: gold   (gold schema)
```

### Database
- **Host:** `localhost:5433` (Docker maps 5433 → 5432 inside container)
- **DB/user/password:** all `postgres` / `yugioh` / `postgres`
- Raw tables live in the `public` schema; dbt layers write to `bronze`, `silver`, and `gold` schemas.

### dbt Layers (`ProjetoDBT/models/`)

| Folder | Schema | Materialization | Purpose |
|--------|--------|----------------|---------|
| `staging/` | `bronze` | table | Thin SELECT over raw source tables — no transformations |
| `marts/` | `silver` | table | Cleaning, validation, EUR→USD currency conversion (rate hardcoded at 1.10), quality flags |
| `gold/` | `gold` | table | Analytical models for business questions |

### Key Gold Models
- **`gold_dim_cards`** / **`gold_dim_archetype`** — dimension tables
- **`gold_market_arbitrage`** — identifies cheapest marketplace per card; highlights overpay amount and spread %
- **`gold_rarity_premium_analysis`** — price premium analysis by card rarity across sets

### Source Data (`src/extract_load.py`)
- Fetches 10 archetypes (Blue-Eyes, Dark Magician, Red-Eyes, Elemental HERO, Cyber Dragon, Toon, Dragonmaid, Branded, Exodia, Sky Striker)
- Deduplicates cards by `id` in memory before inserting
- Prices are collected per marketplace (cardmarket/EUR, tcgplayer/USD, ebay/USD, amazon/USD)
- Script is **destructive on each run** — it drops and recreates the three raw tables (`cards`, `card_prices`, `card_sets`)
