from backend.database.connection import execute_query

def migrar_banco():
    """
    Migra o banco para suportar autenticação de alunos vinculada a clientes.
    """
    schema_clientes = execute_query("PRAGMA table_info(clientes)", is_select=True) or []
    colunas_clientes = [coluna[1] for coluna in schema_clientes]

    if "ultimo_pagamento" not in colunas_clientes:
        execute_query("ALTER TABLE clientes ADD COLUMN ultimo_pagamento TEXT")

    if "periodo_plano" not in colunas_clientes:
        execute_query("ALTER TABLE clientes ADD COLUMN periodo_plano TEXT DEFAULT 'mensal'")

    if "email" not in colunas_clientes:
        execute_query("ALTER TABLE clientes ADD COLUMN email TEXT")

    schema_usuarios = execute_query("PRAGMA table_info(usuarios)", is_select=True) or []
    if not schema_usuarios:
        execute_query(
            """
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
        )
        return

    colunas_usuarios = {coluna[1]: coluna for coluna in schema_usuarios}

    senha_hash_notnull = False
    if "senha_hash" in colunas_usuarios:
        senha_hash_notnull = bool(colunas_usuarios["senha_hash"][3])

    precisa_recriar = senha_hash_notnull or any(
        coluna not in colunas_usuarios
        for coluna in ("cliente_id", "activation_code", "activation_created_at")
    )

    if precisa_recriar:
        execute_query("DROP TABLE IF EXISTS usuarios_novo")
        execute_query(
            """
            CREATE TABLE usuarios_novo (
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
        )
        execute_query(
            """
            INSERT INTO usuarios_novo (id, nome, email, senha_hash, cargo)
            SELECT id, NULL, email, senha_hash, cargo
            FROM usuarios
            """
        )
        execute_query("DROP TABLE usuarios")
        execute_query("ALTER TABLE usuarios_novo RENAME TO usuarios")

    schema_usuarios_final = execute_query("PRAGMA table_info(usuarios)", is_select=True) or []
    colunas_finais = [coluna[1] for coluna in schema_usuarios_final]
    if "nome" not in colunas_finais:
        execute_query("ALTER TABLE usuarios ADD COLUMN nome TEXT")

if __name__ == "__main__":
    migrar_banco()
