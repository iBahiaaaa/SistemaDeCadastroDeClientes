from backend.database.connection import execute_query

def inicializar_banco():
    """
    Cria a tabela de clientes se ela não existir.
    Usa a estrutura centralizada de conexão.
    """
    query = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        whatsapp TEXT,
        endereco TEXT,
        plano TEXT,
        valor_plano REAL,
        data_matricula TEXT,
        data_vencimento TEXT,
        contato_emergencia TEXT,
        status TEXT,
        observacoes TEXT
    )
    """
    if execute_query(query):
        print("Banco de dados e tabela 'clientes' inicializados com sucesso!")
    else:
        print("Erro ao inicializar o banco de dados.")

if __name__ == "__main__":
    inicializar_banco()
