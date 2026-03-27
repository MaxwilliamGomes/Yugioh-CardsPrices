# Yu-Gi-Oh Data Warehouse Documentation Templates

## Model Documentation

### Dimensão - Template
```yaml
- name: dim_example
  description: |
    Dimensão de exemplo
    
    **Granularidade:** 1 linha por [entidade]
    **Atualização:** [Frequência]
    **Proprietário:** [Time]
    
    ## Contexto de Negócio
    [Descrever o problema que resolve]
    
    ## Casos de Uso
    - Filtrar por [dimensão]
    - Agrupar por [dimensão]
```

### Fato - Template
```yaml
- name: fact_example
  description: |
    Fato de exemplo
    
    **Granularidade:** 1 linha por [combinação de chaves]
    **Frequência de Atualização:** [Frequência]
    **Volume Esperado:** [Estimativa]
    **Proprietário:** [Time]
    
    ## Problema de Negócio
    [Descrever cenário respondido]
    
    ## Exemplo de Query
    ```sql
    SELECT * FROM fact_example
    WHERE date >= '2026-03-01'
    ```
```

---

## Sources

```yaml
sources:
  - name: yugioh
    description: |
      Fonte de dados bruta para o DW de Yu-Gi-Oh
      
      **Database:** yugioh
      **Sistema Origem:** [Sistema]
      **Frequência de Sincro:** Diária
      
    tables:
      - name: table_name
        description: Descrição da tabela
        columns:
          - name: column_name
            description: Descrição da coluna
            tests:
              - unique
              - not_null
              - relationships
```

---

## Tags para Organização

**Staging:**
- `staging` - Modelos da camada bronze

**Marts:**
- `silver` - Tabelas transformadas
- `mart` - Tabelas de negócio

**Gold:**
- `gold` - Tabelas analíticas
- `analytics` - Pronto para BI
- `dimension` - Dados mestres
- `fact` - Dados de transação

**Dados:**
- `pii` - Informação pessoal identificável
- `confidential` - Dados sensíveis
- `public` - Dados públicos

---

## Testes de Qualidade

### Testes Genéricos Built-in

```yaml
columns:
  - name: id
    tests:
      - unique
      - not_null
  
  - name: created_at
    tests:
      - not_null
  
  - name: category
    tests:
      - not_null
      - accepted_values:
          values: ['A', 'B', 'C']
  
  - name: foreign_key_id
    tests:
      - relationships:
          to: ref('other_table')
          field: id
```

---

## Documentação de Coluna Chave

```yaml
- name: key_column
  description: |
    👉 **COLUNA CHAVE - USAR PARA JOINS**
    
    Tipo: [PK/FK/Business Key]
    Formato: [Formato da chave]
    Regra de Geração: [Regra]
    
    **Exemplo:**
    ```
    UUID v4 gerado em tempo de carregamento
    ```
    
    **Cuidados:**
    - Nunca é NULL
    - Nunca é alterado
    - Garante unicidade por [período]
```

---

## Versionamento de Modelo

```yaml
- name: model_name
  description: |
    Modelo com versionamento
    
    **Versão Atual:** 2.0
    **Data de Release:** 2026-03-26
    **Mudanças:** 
    - v2.0: Adicionada coluna X, removida coluna Y
    - v1.0: Versão inicial
    
    ⚠️ **Breaking Changes em v2.0:** Coluna Y removida (deprecated em v1.5)
```

---

## Padrão de Nomeação

```
[camada]_[tipo]_[entidade]

Exemplos:
- stg_orders          # Staging
- silver_orders       # Marts (dados limpos)
- gold_order_facts    # Gold (fatos)
- gold_dim_date       # Gold (dimensão)
```

**Camadas:**
- `stg_` = Staging (bronze)
- `silver_` = Marts (transformação)
- `gold_` = Analytics (negócio)

**Tipos:**
- `dim_` = Dimensão
- `` (vazio) = Tabela normal
- `_facts` = Tabelas de fatos

---

## Documentação de Performance

```yaml
- name: large_model
  description: |
    Modelo com volume considerável
    
    **Tamanho Estimado:** [GB]
    **Tempo de Execução:** [tempo]
    **Concorrência:** [threads]
    
    ⚡ **Tips de Performance:**
    - Particionar por data
    - Indexar em [coluna]
    - Usar incremental em produção
```

---

## Deprecated & Sunset

```yaml
- name: old_model
  description: |
    ⚠️ **DEPRECATED - Use {{ref('new_model')}} instead**
    
    **Data de Remoção:** 2026-06-30
    **Alternativa:** 
    - Usar `new_model` ao invés
    - Caminho de migração: [documentar]
    
    ~~Tabela antiga~~ → Usar `new_model`
```

---

**Gerado pela equipe de Data Engineering**
Date: {{ execution_date }}
