# 🚀 Setup MCP PostgreSQL - Yu-Gi-Oh DW

## ✅ O que você precisa fazer

### 1️⃣ Instalar dependências

```bash
pip install mcp psycopg2-binary
```

### 2️⃣ Configurar no VS Code

No VS Code, abra as configurações do Copilot:
- Pressione `Ctrl+Shift+P`
- Digite "Open User Settings (JSON)"
- Cole a configuração abaixo (ou mescle se já houver mcpServers):

```json
{
  "claude.mcpServers": {
    "postgres-dw": {
      "command": "python",
      "args": ["mcp_postgres_server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

### 3️⃣ Garantir que PostgreSQL está rodando

```bash
docker-compose up -d
```

Verifique se está rodando:
```bash
docker ps | grep postgres
```

### 4️⃣ Reiniciar o VS Code

Depois de salvar as configurações, reinicie o VS Code para carregar o MCP.

## 🎯 Como usar

No Copilot Chat, você pode agora:

```
"Quantos cards temos no banco de dados?"
"Quais são os cards mais caros?"
"Mostra todos os decks de Blue-Eyes"
"Qual é a estrutura das tabelas?"
"Quantos cards de cada tipo temos?"
```

## 🔧 Ferramentas disponíveis

### 1. `query_database`
Executa queries SQL direto no PostgreSQL

**Exemplo:**
```sql
SELECT name, card_type, price FROM cards WHERE card_type = 'Monster' LIMIT 10
```

### 2. `get_database_schema`
Mostra a estrutura de todas as tabelas

### 3. `analyze_data`
Faz análises rápidas no DW

## 🐛 Troubleshooting

### Erro: "Could not connect to PostgreSQL"
- Verifique se Docker está rodando: `docker ps`
- Reinicie: `docker-compose down && docker-compose up -d`

### Erro: "ModuleNotFoundError: mcp"
- Reinstale: `pip install --upgrade mcp`

### Copilot não vê o MCP
- Verifique settings.json do VS Code
- Restart VS Code completamente
- Abra o terminal integrado e rode manualmente para ver erros: `python mcp_postgres_server.py`

## 📊 Próximos passos

Se quiser adicionar mais ferramentas (relatórios, dashboards, etc), edite o arquivo `mcp_postgres_server.py`.

Enjoy! 🎮🗄️
