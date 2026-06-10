from backend.database.connection import execute_query

def ver_clientes():
    """
    Script utilitário para listar todos os clientes no console.
    """
    query = "SELECT * FROM clientes"
    clientes = execute_query(query, is_select=True)

    if clientes:
        print(f"{'ID':<4} | {'Nome':<20} | {'Status':<10}")
        print("-" * 40)
        for cliente in clientes:
            # cliente[0] = id, cliente[1] = nome, cliente[10] = status
            print(f"{cliente[0]:<4} | {cliente[1]:<20} | {cliente[10]:<10}")
    else:
        print("Nenhum cliente cadastrado ou erro na consulta.")

if __name__ == "__main__":
    ver_clientes()
