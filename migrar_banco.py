from backend.database.connection import execute_query

def migrar_banco():
    """
    Adiciona os novos campos (ultimo_pagamento, periodo_plano) na tabela clientes.
    """
    # Obter o schema atual da tabela
    query_schema = "PRAGMA table_info(clientes)"
    schema = execute_query(query_schema, is_select=True)
    
    colunas_existentes = [coluna[1] for coluna in schema] if schema else []
    
    # Verificar e adicionar ultimo_pagamento
    if 'ultimo_pagamento' not in colunas_existentes:
        query_adicionar_ultimo_pagamento = "ALTER TABLE clientes ADD COLUMN ultimo_pagamento TEXT"
        if execute_query(query_adicionar_ultimo_pagamento):
            print("Campo 'ultimo_pagamento' adicionado com sucesso!")
    else:
        print("Campo 'ultimo_pagamento' já existe.")
    
    # Verificar e adicionar periodo_plano
    if 'periodo_plano' not in colunas_existentes:
        query_adicionar_periodo_plano = "ALTER TABLE clientes ADD COLUMN periodo_plano TEXT DEFAULT 'mensal'"
        if execute_query(query_adicionar_periodo_plano):
            print("Campo 'periodo_plano' adicionado com sucesso!")
    else:
        print("Campo 'periodo_plano' já existe.")

if __name__ == "__main__":
    migrar_banco()