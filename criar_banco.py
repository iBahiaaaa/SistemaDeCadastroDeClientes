import sqlite3

conexao = sqlite3.connect("banco.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    whatsapp TEXT,
    endereco TEXT,
    observacoes TEXT
)
""")

conexao.commit()
conexao.close()

print("Banco criado com sucesso!")