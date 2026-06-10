from backend.database.connection import execute_query


def salvar_cliente(
    nome,
    whatsapp,
    endereco,
    plano,
    valor_plano,
    data_matricula,
    data_vencimento,
    contato_emergencia,
    status,
    observacoes
):
    """
    Insere um novo cliente no banco de dados.
    """

    query = """
        INSERT INTO clientes (
            nome,
            whatsapp,
            endereco,
            plano,
            valor_plano,
            data_matricula,
            data_vencimento,
            contato_emergencia,
            status,
            observacoes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        nome,
        whatsapp,
        endereco,
        plano,
        valor_plano,
        data_matricula,
        data_vencimento,
        contato_emergencia,
        status,
        observacoes
    )

    return execute_query(query, params)


def buscar_clientes():
    """
    Retorna todos os clientes cadastrados.
    """

    query = """
        SELECT
            id,
            nome,
            whatsapp,
            endereco,
            plano,
            valor_plano,
            data_matricula,
            data_vencimento,
            contato_emergencia,
            status,
            observacoes
        FROM clientes
        ORDER BY nome
    """

    return execute_query(query, is_select=True)


def buscar_cliente_por_id(id_cliente):
    """
    Busca um cliente específico pelo ID.
    """

    query = """
        SELECT
            id,
            nome,
            whatsapp,
            endereco,
            plano,
            valor_plano,
            data_matricula,
            data_vencimento,
            contato_emergencia,
            status,
            observacoes
        FROM clientes
        WHERE id = ?
    """

    resultado = execute_query(query, (id_cliente,), is_select=True)

    if resultado:
        return resultado[0]

    return None


def atualizar_cliente(
    id_cliente,
    nome,
    whatsapp,
    endereco,
    plano,
    valor_plano,
    data_matricula,
    data_vencimento,
    contato_emergencia,
    status,
    observacoes
):
    """
    Atualiza um cliente existente.
    """

    query = """
        UPDATE clientes
        SET
            nome = ?,
            whatsapp = ?,
            endereco = ?,
            plano = ?,
            valor_plano = ?,
            data_matricula = ?,
            data_vencimento = ?,
            contato_emergencia = ?,
            status = ?,
            observacoes = ?
        WHERE id = ?
    """

    params = (
        nome,
        whatsapp,
        endereco,
        plano,
        valor_plano,
        data_matricula,
        data_vencimento,
        contato_emergencia,
        status,
        observacoes,
        id_cliente
    )

    return execute_query(query, params)


def excluir_cliente(id_cliente):
    """
    Exclui um cliente pelo ID.
    """

    query = "DELETE FROM clientes WHERE id = ?"

    return execute_query(query, (id_cliente,))