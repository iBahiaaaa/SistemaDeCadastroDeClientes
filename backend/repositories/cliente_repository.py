from backend.database.connection import execute_query
from datetime import datetime, timedelta
import secrets


def calcular_status_automatico(data_vencimento):
    """
    Calcula o status do cliente automaticamente com base na data de vencimento:
    - Pago: se data de vencimento for >= hoje
    - Pendente: se data de vencimento for ontem ou até 7 dias atrás
    - Inadimplente: se data de vencimento for mais de 7 dias atrás
    """
    hoje = datetime.now().date()
    
    if not data_vencimento:
        return "Pendente"
        
    try:
        data_venc = datetime.strptime(data_vencimento, "%Y-%m-%d").date()
        diferenca_dias = (hoje - data_venc).days
        
        if diferenca_dias <= 0:
            return "Pago"
        elif 1 <= diferenca_dias <= 7:
            return "Pendente"
        else:
            return "Inadimplente"
            
    except ValueError:
        return "Pendente"


def calcular_data_vencimento(data_referencia, periodo_plano):
    """
    Calcula a próxima data de vencimento com base na data de referência e período do plano
    Períodos suportados: mensal, trimestral, semestral, anual
    """
    if not data_referencia:
        return None
        
    try:
        data = datetime.strptime(data_referencia, "%Y-%m-%d")
        
        if periodo_plano == "trimestral":
            # Adiciona 3 meses
            mes = data.month + 2
            ano = data.year
            dia = data.day
            
            if mes > 12:
                mes -= 12
                ano += 1
                
            nova_data = datetime(ano, mes, dia)
            return nova_data.strftime("%Y-%m-%d")
            
        elif periodo_plano == "semestral":
            # Adiciona 6 meses
            mes = data.month + 5
            ano = data.year
            dia = data.day
            
            if mes > 12:
                mes -= 12
                ano += 1
                
            nova_data = datetime(ano, mes, dia)
            return nova_data.strftime("%Y-%m-%d")
            
        elif periodo_plano == "anual":
            # Adiciona 1 ano
            nova_data = datetime(data.year + 1, data.month, data.day)
            return nova_data.strftime("%Y-%m-%d")
            
        else:  # Padrão: mensal
            # Adiciona 1 mês
            mes = data.month + 1
            ano = data.year
            dia = data.day
            
            if mes > 12:
                mes = 1
                ano += 1
                
            # Trata casos como 31 de janeiro para fevereiro (evita erro)
            while True:
                try:
                    nova_data = datetime(ano, mes, dia)
                    break
                except ValueError:
                    dia -= 1
                    
            return nova_data.strftime("%Y-%m-%d")
            
    except ValueError:
        return None


def salvar_cliente(
    nome,
    email,
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
            email,
            whatsapp,
            endereco,
            plano,
            valor_plano,
            data_matricula,
            data_vencimento,
            ultimo_pagamento,
            contato_emergencia,
            status,
            observacoes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)
    """

    params = (
        nome,
        email,
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

    return execute_query(query, params, return_lastrowid=True)


def buscar_clientes():
    """
    Retorna todos os clientes cadastrados com status calculado automaticamente.
    """

    query = """
        SELECT
            c.id,
            c.nome,
            c.email,
            c.whatsapp,
            c.endereco,
            c.plano,
            c.valor_plano,
            c.data_matricula,
            c.data_vencimento,
            c.ultimo_pagamento,
            c.contato_emergencia,
            c.observacoes,
            (SELECT u.activation_code FROM usuarios u WHERE u.cliente_id = c.id) AS activation_code,
            (SELECT CASE WHEN u.senha_hash IS NOT NULL AND u.senha_hash <> '' THEN 1 ELSE 0 END FROM usuarios u WHERE u.cliente_id = c.id) AS conta_ativa
        FROM clientes c
        ORDER BY nome
    """

    clientes = execute_query(query, is_select=True)

    if not clientes or clientes is None:
        return []

    # Calcula status automaticamente para cada cliente
    clientes_com_status = []
    for cliente in clientes:
        cliente_dict = dict(cliente)  # Converte para dicionário
        cliente_dict['status'] = calcular_status_automatico(cliente_dict['data_vencimento'])
        clientes_com_status.append(cliente_dict)

    return clientes_com_status


def buscar_cliente_por_id(id_cliente):
    """
    Busca um cliente pelo seu ID.
    """

    query = """
        SELECT
            c.id,
            c.nome,
            c.email,
            c.whatsapp,
            c.endereco,
            c.plano,
            c.valor_plano,
            c.data_matricula,
            c.data_vencimento,
            c.ultimo_pagamento,
            c.contato_emergencia,
            c.observacoes,
            (SELECT u.activation_code FROM usuarios u WHERE u.cliente_id = c.id) AS activation_code,
            (SELECT CASE WHEN u.senha_hash IS NOT NULL AND u.senha_hash <> '' THEN 1 ELSE 0 END FROM usuarios u WHERE u.cliente_id = c.id) AS conta_ativa
        FROM clientes c
        WHERE c.id = ?
    """

    resultado = execute_query(query, (id_cliente,), is_select=True)

    if resultado:
        return resultado[0]

    return None


def buscar_nome_cliente_por_id(id_cliente):
    resultado = execute_query(
        "SELECT nome FROM clientes WHERE id = ?",
        (id_cliente,),
        is_select=True
    )
    if not resultado:
        return None
    return dict(resultado[0]).get("nome")


def buscar_cliente_por_email(email):
    if not email:
        return None

    resultado = execute_query(
        "SELECT id, nome, email FROM clientes WHERE LOWER(email) = ? LIMIT 1",
        (email.strip().lower(),),
        is_select=True
    )
    if not resultado:
        return None
    return dict(resultado[0])


def atualizar_cliente(
    id_cliente,
    nome,
    email,
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
            email = ?,
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
        email,
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


def pesquisar_clientes(termo_pesquisa):
    """
    Pesquisa clientes por todos os campos.
    """

    query = """
        SELECT
            c.id,
            c.nome,
            c.email,
            c.whatsapp,
            c.endereco,
            c.plano,
            c.valor_plano,
            c.data_matricula,
            c.data_vencimento,
            c.ultimo_pagamento,
            c.contato_emergencia,
            c.observacoes,
            (SELECT u.activation_code FROM usuarios u WHERE u.cliente_id = c.id) AS activation_code,
            (SELECT CASE WHEN u.senha_hash IS NOT NULL AND u.senha_hash <> '' THEN 1 ELSE 0 END FROM usuarios u WHERE u.cliente_id = c.id) AS conta_ativa
        FROM clientes c
        WHERE 
            c.nome LIKE ? OR
            c.email LIKE ? OR
            c.whatsapp LIKE ? OR
            c.endereco LIKE ? OR
            c.plano LIKE ? OR
            c.valor_plano LIKE ? OR
            c.data_matricula LIKE ? OR
            c.data_vencimento LIKE ? OR
            c.contato_emergencia LIKE ? OR
            c.observacoes LIKE ?
        ORDER BY nome
    """

    termo = f"%{termo_pesquisa}%"
    params = (termo, termo, termo, termo, termo, termo, termo, termo, termo, termo)

    clientes = execute_query(query, params, is_select=True)

    if not clientes or clientes is None:
        return []

    # Calcula status automaticamente para cada cliente
    clientes_com_status = []
    for cliente in clientes:
        cliente_dict = dict(cliente)  # Converte para dicionário
        cliente_dict['status'] = calcular_status_automatico(cliente_dict['data_vencimento'])
        clientes_com_status.append(cliente_dict)

    return clientes_com_status


def registrar_pagamento(id_cliente):
    """
    Registra um pagamento:
    1. Salva a data de vencimento atual em ultimo_pagamento
    2. Calcula a nova data de vencimento usando ultimo_pagamento como base
    """
    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        return False
        
    cliente_dict = dict(cliente)
    data_vencimento_atual = cliente_dict.get('data_vencimento')
    plano = cliente_dict.get('plano', 'mensal')
    
    if data_vencimento_atual:
        # Calcula a nova data de vencimento
        nova_data_vencimento = calcular_data_vencimento(data_vencimento_atual, plano)
        
        if nova_data_vencimento:
            query = """
                UPDATE clientes
                SET
                    ultimo_pagamento = ?,
                    data_vencimento = ?,
                    status = 'Pago'
                WHERE id = ?
            """
            
            params = (data_vencimento_atual, nova_data_vencimento, id_cliente)
            return execute_query(query, params)
    
    return False


def email_em_uso_em_outro_cliente(email, id_cliente=None):
    if not email:
        return False

    email = email.strip().lower()
    if id_cliente:
        resultado = execute_query(
            "SELECT id FROM clientes WHERE LOWER(email) = ? AND id <> ? LIMIT 1",
            (email, id_cliente),
            is_select=True
        )
    else:
        resultado = execute_query(
            "SELECT id FROM clientes WHERE LOWER(email) = ? LIMIT 1",
            (email,),
            is_select=True
        )

    return bool(resultado)


def email_em_uso_em_usuario(email, cliente_id=None):
    if not email:
        return False

    email = email.strip().lower()
    if cliente_id:
        resultado = execute_query(
            "SELECT id FROM usuarios WHERE LOWER(email) = ? AND (cliente_id IS NULL OR cliente_id <> ?) LIMIT 1",
            (email, cliente_id),
            is_select=True
        )
    else:
        resultado = execute_query(
            "SELECT id FROM usuarios WHERE LOWER(email) = ? LIMIT 1",
            (email,),
            is_select=True
        )

    return bool(resultado)


def garantir_conta_aluno(cliente_id, email):
    if not email:
        return True

    email = email.strip().lower()

    existente = execute_query(
        "SELECT id, email, senha_hash FROM usuarios WHERE cliente_id = ? LIMIT 1",
        (cliente_id,),
        is_select=True
    )

    if existente:
        usuario = dict(existente[0])
        if (usuario.get("email") or "").strip().lower() != email:
            if email_em_uso_em_usuario(email, cliente_id=cliente_id):
                return None
            return execute_query(
                "UPDATE usuarios SET email = ? WHERE id = ?",
                (email, usuario["id"])
            )
        return True

    if email_em_uso_em_usuario(email):
        return None

    codigo = secrets.token_urlsafe(6)
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return execute_query(
        """
        INSERT INTO usuarios (email, senha_hash, cargo, cliente_id, activation_code, activation_created_at)
        VALUES (?, NULL, 'ALUNO', ?, ?, ?)
        """,
        (email, cliente_id, codigo, criado_em)
    )
