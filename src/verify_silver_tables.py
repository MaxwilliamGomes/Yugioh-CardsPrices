import psycopg2
import psycopg2.extras

conn = psycopg2.connect(host='localhost', port='5433', database='yugioh', user='postgres', password='postgres')
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("=" * 70)
print("📊 VERIFICACAO DAS TABELAS SILVER")
print("=" * 70)

tabelas = [
    ('silver', 'silver_cards'),
    ('silver', 'silver_card_prices'),
    ('silver', 'silver_card_sets'),
]

for schema, tabela in tabelas:
    cursor.execute(f"SELECT COUNT(*) FROM {schema}.{tabela}")
    count = cursor.fetchone()['count']
    
    # Pegar nomes das colunas
    cursor.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = '{schema}' AND table_name = '{tabela}'
        ORDER BY ordinal_position
    """)
    cols = [row['column_name'] for row in cursor.fetchall()]
    
    print(f"\n✅ {schema}.{tabela}")
    print(f"   Registros: {count}")
    print(f"   Colunas ({len(cols)}): {', '.join(cols[:5])}{'...' if len(cols) > 5 else ''}")
    
    # Mostrar exemplo
    cursor.execute(f"SELECT * FROM {schema}.{tabela} LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"   Exemplo: {dict(row)}")

conn.close()
print("\n" + "=" * 70)
print("✅ SETUP DBT CONCLUÍDO COM SUCESSO!")
print("=" * 70)
