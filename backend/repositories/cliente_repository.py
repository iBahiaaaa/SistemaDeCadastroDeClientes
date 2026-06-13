from backend.database.connection import get_supabase
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
            mes = data.month + 2
            ano = data.year
            dia = data.day
            
            if mes > 12:
                mes -= 12
                ano += 1
                
            nova_data = datetime(ano, mes, dia)
            return nova_data.strftime("%Y-%m-%d")
            
        elif periodo_plano == "semestral":
            mes = data.month + 5
            ano = data.year
            dia = data.day
            
            if mes > 12:
                mes -= 12
                ano += 1
                
            nova_data = datetime(ano, mes, dia)
            return nova_data.strftime("%Y-%m-%d")
            
        elif periodo_plano == "anual":
            nova_data = datetime(data.year + 1, data.month, data.day)
            return nova_data.strftime("%Y-%m-%d")
            
        else:
            mes = data.month + 1
            ano = data.year
            dia = data.day
            
            if mes > 12:
                mes = 1
                ano += 1
                
            while True:
                try:
                    nova_data = datetime(ano, mes, dia)
                    break
                except ValueError:
                    dia -= 1
                    
            return nova_data.strftime("%Y-%m-%d")
            
    except ValueError:
        return None


def salvar_cliente(nome, email, whatsapp, endereco, plano, valor_plano, data_matricula, data_vencimento, contato_emergencia, status, observacoes):
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .insert({
            "nome": nome,
            "email": email,
            "whatsapp": whatsapp,
            "endereco": endereco,
            "plano": plano,
            "valor_plano": valor_plano,
            "periodo_plano": plano or "mensal",
            "data_matricula": data_matricula,
            "data_vencimento": data_vencimento,
            "contato_emergencia": contato_emergencia,
            "status": status,
            "observacoes": observacoes
        })
        .execute()
    )
    
    return result.data[0]["id"] if result.data else None


def buscar_clientes():
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .select("*, usuarios!clientes_cliente_id_fkey(activation_code, senha_hash)")
        .order("nome")
        .execute()
    )
    
    clientes = []
    for cliente in result.data or []:
        cliente_dict = dict(cliente)
        cliente_dict["status"] = calcular_status_automatico(cliente_dict.get("data_vencimento"))
        
        # Ajusta os campos da conta do usuário
        usuario = cliente_dict.pop("usuarios", [])
        if usuario:
            cliente_dict["activation_code"] = usuario[0].get("activation_code")
            cliente_dict["conta_ativa"] = 1 if usuario[0].get("senha_hash") else 0
        else:
            cliente_dict["activation_code"] = None
            cliente_dict["conta_ativa"] = 0
            
        clientes.append(cliente_dict)
        
    return clientes


def buscar_cliente_por_id(id_cliente):
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .select("*, usuarios!clientes_cliente_id_fkey(activation_code, senha_hash)")
        .eq("id", id_cliente)
        .execute()
    )
    
    if not result.data:
        return None
        
    cliente = dict(result.data[0])
    cliente["status"] = calcular_status_automatico(cliente.get("data_vencimento"))
    
    usuario = cliente.pop("usuarios", [])
    if usuario:
        cliente["activation_code"] = usuario[0].get("activation_code")
        cliente["conta_ativa"] = 1 if usuario[0].get("senha_hash") else 0
    else:
        cliente["activation_code"] = None
        cliente["conta_ativa"] = 0
        
    return cliente


def buscar_nome_cliente_por_id(id_cliente):
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .select("nome")
        .eq("id", id_cliente)
        .execute()
    )
    
    return result.data[0]["nome"] if result.data else None


def buscar_cliente_por_email(email):
    if not email:
        return None

    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .select("id, nome, email")
        .ilike("email", email.strip().lower())
        .limit(1)
        .execute()
    )
    
    return result.data[0] if result.data else None


def atualizar_cliente(id_cliente, nome, email, whatsapp, endereco, plano, valor_plano, data_matricula, data_vencimento, contato_emergencia, status, observacoes):
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .update({
            "nome": nome,
            "email": email,
            "whatsapp": whatsapp,
            "endereco": endereco,
            "plano": plano,
            "valor_plano": valor_plano,
            "periodo_plano": plano or "mensal",
            "data_matricula": data_matricula,
            "data_vencimento": data_vencimento,
            "contato_emergencia": contato_emergencia,
            "status": status,
            "observacoes": observacoes
        })
        .eq("id", id_cliente)
        .execute()
    )
    
    return len(result.data) > 0


def excluir_cliente(id_cliente):
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .delete()
        .eq("id", id_cliente)
        .execute()
    )
    
    return len(result.data) > 0


def pesquisar_clientes(termo_pesquisa):
    supabase = get_supabase()
    
    # Supabase não suporta OR com LIKE diretamente em um único query facilmente,
    # então vamos usar .or() com os campos
    result = (
        supabase.table("clientes")
        .select("*, usuarios!clientes_cliente_id_fkey(activation_code, senha_hash)")
        .or_(
            f"nome.ilike.%{termo_pesquisa}%,"
            f"email.ilike.%{termo_pesquisa}%,"
            f"whatsapp.ilike.%{termo_pesquisa}%,"
            f"endereco.ilike.%{termo_pesquisa}%,"
            f"plano.ilike.%{termo_pesquisa}%,"
            f"valor_plano.ilike.%{termo_pesquisa}%,"
            f"data_matricula.ilike.%{termo_pesquisa}%,"
            f"data_vencimento.ilike.%{termo_pesquisa}%,"
            f"contato_emergencia.ilike.%{termo_pesquisa}%,"
            f"observacoes.ilike.%{termo_pesquisa}%"
        )
        .order("nome")
        .execute()
    )
    
    clientes = []
    for cliente in result.data or []:
        cliente_dict = dict(cliente)
        cliente_dict["status"] = calcular_status_automatico(cliente_dict.get("data_vencimento"))
        
        usuario = cliente_dict.pop("usuarios", [])
        if usuario:
            cliente_dict["activation_code"] = usuario[0].get("activation_code")
            cliente_dict["conta_ativa"] = 1 if usuario[0].get("senha_hash") else 0
        else:
            cliente_dict["activation_code"] = None
            cliente_dict["conta_ativa"] = 0
            
        clientes.append(cliente_dict)
        
    return clientes


def registrar_pagamento(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        return False
        
    data_vencimento_atual = cliente.get("data_vencimento")
    plano = cliente.get("plano", "mensal")
    
    if data_vencimento_atual:
        nova_data_vencimento = calcular_data_vencimento(data_vencimento_atual, plano)
        
        if nova_data_vencimento:
            supabase = get_supabase()
            result = (
                supabase.table("clientes")
                .update({
                    "ultimo_pagamento": data_vencimento_atual,
                    "data_vencimento": nova_data_vencimento,
                    "status": "Pago"
                })
                .eq("id", id_cliente)
                .execute()
            )
            
            return len(result.data) > 0
    
    return False


def email_em_uso_em_outro_cliente(email, id_cliente=None):
    if not email:
        return False

    email = email.strip().lower()
    supabase = get_supabase()
    
    query = supabase.table("clientes").select("id").ilike("email", email)
    if id_cliente:
        query = query.neq("id", id_cliente)
    
    result = query.limit(1).execute()
    
    return len(result.data) > 0


def email_em_uso_em_usuario(email, cliente_id=None):
    if not email:
        return False

    email = email.strip().lower()
    supabase = get_supabase()
    
    query = supabase.table("usuarios").select("id").ilike("email", email)
    if cliente_id:
        query = query.or_(f"cliente_id.is.null,cliente_id.neq.{cliente_id}")
    
    result = query.limit(1).execute()
    
    return len(result.data) > 0


def garantir_conta_aluno(cliente_id, email):
    if not email:
        return True

    email = email.strip().lower()
    supabase = get_supabase()
    
    # Verifica se já existe usuário vinculado a esse cliente
    result = (
        supabase.table("usuarios")
        .select("id, email, senha_hash")
        .eq("cliente_id", cliente_id)
        .limit(1)
        .execute()
    )
    
    if result.data:
        usuario = result.data[0]
        if (usuario.get("email") or "").strip().lower() != email:
            if email_em_uso_em_usuario(email, cliente_id=cliente_id):
                return None
            # Atualiza o email do usuário
            supabase.table("usuarios").update({"email": email}).eq("id", usuario["id"]).execute()
        return True
    
    # Cria novo usuário
    if email_em_uso_em_usuario(email):
        return None
        
    codigo = secrets.token_urlsafe(6)
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = (
        supabase.table("usuarios")
        .insert({
            "email": email,
            "senha_hash": None,
            "cargo": "ALUNO",
            "cliente_id": cliente_id,
            "activation_code": codigo,
            "activation_created_at": criado_em
        })
        .execute()
    )
    
    return len(result.data) > 0
