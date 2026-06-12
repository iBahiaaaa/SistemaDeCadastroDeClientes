from backend.database.connection import execute_query

def inicializar_banco():
    """
    Cria as tabelas do sistema se elas não existirem.
    Usa a estrutura centralizada de conexão.
    """
    query_clientes = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        whatsapp TEXT,
        endereco TEXT,
        plano TEXT,
        valor_plano REAL,
        periodo_plano TEXT DEFAULT 'mensal',
        data_matricula TEXT,
        data_vencimento TEXT,
        ultimo_pagamento TEXT,
        contato_emergencia TEXT,
        status TEXT,
        observacoes TEXT
    )
    """
    query_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT NOT NULL UNIQUE,
        senha_hash TEXT,
        cargo TEXT NOT NULL CHECK (
            cargo IN ('ADM', 'FUNCIONARIO', 'INSTRUTOR', 'FINANCEIRO', 'ALUNO')
        ),
        cliente_id INTEGER UNIQUE,
        activation_code TEXT,
        activation_created_at TEXT
    )
    """

    ok_clientes = bool(execute_query(query_clientes))
    ok_usuarios = bool(execute_query(query_usuarios))

    if ok_clientes and ok_usuarios:
        print("Banco de dados e tabelas inicializados com sucesso!")
    else:
        print("Erro ao inicializar o banco de dados.")

if __name__ == "__main__":
    inicializar_banco()
