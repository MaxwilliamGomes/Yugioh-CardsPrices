#!/usr/bin/env python3
"""
MCP Server para PostgreSQL - permite consultar DW via Copilot no VS Code
"""

import psycopg2
import psycopg2.extras
import json
from typing import Any
from mcp.server import Server, Request
from mcp.types import Tool, TextContent, ToolResponse

# ⚙️ CONFIG DO BANCO
DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "database": "yugioh",
    "user": "postgres",
    "password": "postgres"
}

# 🔌 Criar servidor MCP
server = Server("postgres-dw")

# 🔗 Conexão com o banco
def get_db_connection():
    """Estabelece conexão com PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

def execute_query(query: str) -> dict:
    """Executa uma query SQL e retorna resultados em JSON"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Permitir múltiplas queries separadas por ;
        for single_query in query.split(';'):
            single_query = single_query.strip()
            if not single_query:
                continue
                
            cursor.execute(single_query)
            
            # Se é SELECT, retorna dados
            if single_query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                conn.close()
                return {
                    "status": "success",
                    "rows": [dict(row) for row in results],
                    "count": len(results)
                }
        
        # Para INSERT/UPDATE/DELETE
        conn.commit()
        conn.close()
        return {
            "status": "success",
            "rows_affected": cursor.rowcount,
            "message": "Operação executada com sucesso"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def get_table_schema() -> dict:
    """Retorna estrutura de todas as tabelas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = """
        SELECT 
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        # Organizar por tabela
        schema = {}
        for row in results:
            table = row['table_name']
            if table not in schema:
                schema[table] = []
            schema[table].append({
                "column": row['column_name'],
                "type": row['data_type'],
                "nullable": row['is_nullable']
            })
        
        return {
            "status": "success",
            "schema": schema
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

# 📋 FERRAMENTAS DO MCP

@server.list_tools()
async def list_tools():
    """Lista ferramentas disponíveis"""
    return [
        Tool(
            name="query_database",
            description="Executa uma query SQL no PostgreSQL e retorna os resultados. Útil para buscar, inserir, atualizar ou deletar dados.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "Query SQL a executar (ex: SELECT * FROM cards WHERE name LIKE '%Dark%')"
                    }
                },
                "required": ["sql"]
            }
        ),
        Tool(
            name="get_database_schema",
            description="Retorna a estrutura de todas as tabelas do banco de dados, com colunas e tipos de dados.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="analyze_data",
            description="Executa análises comuns no DW (contagens, agregações, etc)",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_type": {
                        "type": "string",
                        "enum": ["table_counts", "column_stats", "top_cards", "deck_stats"],
                        "description": "Tipo de análise a realizar"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Nome da tabela (se aplicável)"
                    }
                },
                "required": ["analysis_type"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> ToolResponse:
    """Processa chamadas de ferramentas"""
    
    if name == "query_database":
        sql = arguments.get("sql", "")
        result = execute_query(sql)
        result_text = json.dumps(result, indent=2, ensure_ascii=False, default=str)
        return ToolResponse(
            content=[TextContent(type="text", text=result_text)]
        )
    
    elif name == "get_database_schema":
        result = get_table_schema()
        result_text = json.dumps(result, indent=2, ensure_ascii=False, default=str)
        return ToolResponse(
            content=[TextContent(type="text", text=result_text)]
        )
    
    elif name == "analyze_data":
        analysis_type = arguments.get("analysis_type")
        table_name = arguments.get("table_name", "")
        
        analyzed_result = ""
        
        if analysis_type == "table_counts":
            result = execute_query("""
                SELECT table_name, 
                       (xpath('/row', query_to_xml(format('SELECT COUNT(*) FROM %I', table_name), true, true, '')))[1]::text::int as count
                FROM information_schema.schemata sch
                JOIN information_schema.tables t ON sch.oid = t.table_schema::regnamespace
                WHERE table_schema = 'public'
            """)
            analyzed_result = json.dumps(result, indent=2, ensure_ascii=False, default=str)
        
        elif analysis_type in ["column_stats", "top_cards"]:
            # Tenta buscar informações úteis
            result = get_table_schema()
            analyzed_result = json.dumps(result, indent=2, ensure_ascii=False, default=str)
        
        return ToolResponse(
            content=[TextContent(type="text", text=analyzed_result)]
        )
    
    else:
        return ToolResponse(
            content=[TextContent(type="text", text=f"Ferramenta desconhecida: {name}")]
        )

async def main():
    """Inicia o servidor MCP"""
    async with server:
        print("🚀 MCP PostgreSQL Server iniciado!")
        print(f"📊 Conectado a: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        await server.wait_for_shutdown()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
