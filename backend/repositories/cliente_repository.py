import sqlite3


def salvar_cliente(
    nome,
    whatsapp,
    endereco,
    observacoes
):

    conexao = sqlite3.connect("backend/database/banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nome, whatsapp, endereco, observacoes)
        VALUES (?, ?, ?, ?)
    """, (nome, whatsapp, endereco, observacoes))

    conexao.commit()
    conexao.close()
    
def buscar_clientes():

    conexao = sqlite3.connect("backend/database/banco.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")

    clientes = cursor.fetchall()

    conexao.close()

    return clientes