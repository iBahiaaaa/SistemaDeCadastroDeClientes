import sqlite3
import os

DB_TYPE = "SQLITE"
DB_PATH = os.path.join("backend", "database", "banco.db")


def get_connection():
    """
    Retorna uma conexão com o banco de dados.
    """

    if DB_TYPE == "SQLITE":
        try:
            conexao = sqlite3.connect(DB_PATH)

            # Permite acessar colunas pelo nome
            conexao.row_factory = sqlite3.Row

            return conexao

        except sqlite3.Error as e:
            print(f"Erro ao conectar ao SQLite: {e}")
            return None

    elif DB_TYPE == "POSTGRES":
        raise NotImplementedError(
            "Conexão com PostgreSQL ainda não implementada."
        )

    return None


def close_connection(conexao):
    """
    Fecha a conexão com o banco.
    """

    if conexao:
        conexao.close()


def execute_query(query, params=(), is_select=False, return_lastrowid=False):
    """
    Executa uma query.
    """

    conexao = get_connection()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor()
        cursor.execute(query, params)

        if is_select:
            return cursor.fetchall()

        conexao.commit()
        if return_lastrowid:
            return cursor.lastrowid
        return True

    except Exception as e:
        print(f"Erro ao executar query: {e}")

        try:
            conexao.rollback()
        except:
            pass

        return None

    finally:
        close_connection(conexao)
