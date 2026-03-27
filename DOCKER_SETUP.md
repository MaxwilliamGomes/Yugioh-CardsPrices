# Configuração do Postgres com Docker

## Pré-requisitos
- Docker e Docker Compose instalados
- Python 3.12+ com psycopg2 (✅ já instalado)

## Como usar

### 1. Iniciar o Postgres
```bash
docker-compose up -d
```

Isso irá:
- Baixar a imagem do Postgres 15 Alpine (leve)
- Criar um container chamado `yugioh_postgres`
- Expor na porta `5432`
- Criar um volume para persistência de dados

### 2. Verificar o status
```bash
docker-compose ps
```

Aguarde até ver o status `healthy` (pode levar 10-20 segundos).

### 3. Executar o script de extração
```bash
python src/extract_load.py
```

O script irá:
- Buscar dados da API YGO Pro Deck
- Criar as tabelas automaticamente
- Inserir cartas e preços no Postgres

### 4. Parar o Postgres
```bash
docker-compose down
```

## Credenciais do Banco
- **Host:** localhost
- **Port:** 5432
- **User:** postgres
- **Password:** postgres
- **Database:** yugioh

## Conectar ao Postgres manualmente

### Via psql (linha de comando)
```bash
psql -h localhost -U postgres -d yugioh
```

Senha: `postgres`

### SQL útil
```sql
-- Ver cartas
SELECT * FROM cards LIMIT 10;

-- Ver preços
SELECT * FROM card_prices LIMIT 10;

-- Contar registros
SELECT COUNT(*) FROM cards;
SELECT COUNT(*) FROM card_prices;

-- Ver preços de uma carta específica
SELECT c.name, cp.marketplace, cp.price, cp.currency 
FROM cards c
JOIN card_prices cp ON c.id = cp.card_id
WHERE c.name LIKE '%Blue%'
LIMIT 10;
```

## Troubleshooting

**Erro: "could not connect to server"**
- Certifique-se que Docker está rodando
- Execute `docker-compose up -d` novamente

**Erro: "database does not exist"**
- Aguarde alguns segundos após `docker-compose up -d`
- Verifique com `docker-compose ps`

**Limpar tudo e recomeçar**
```bash
docker-compose down -v
docker-compose up -d
```
