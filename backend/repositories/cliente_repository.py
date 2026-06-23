from backend.database.connection import get_supabase
from datetime import datetime, timedelta
import secrets
import re


def limpar_valor_monetario(valor):
    if not valor:
        return None
    valor_str = str(valor).strip()
    # Remove R$, espaços, pontos de milhar
    valor_limpo = re.sub(r'[R$\s.]', '', valor_str)
    # Troca vírgula por ponto
    valor_limpo = valor_limpo.replace(',', '.')
    try:
        return float(valor_limpo)
    except ValueError:
        return None


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


def calcular_data_vencimento(data_referencia, periodo_plano, dia_base=None):
    """
    Calcula a próxima data de vencimento com base na data de referência e período do plano
    Sempre mantém o dia base (se fornecido, tipicamente o dia da matrícula)
    Períodos suportados: mensal, trimestral, semestral, anual
    """
    if not data_referencia:
        return None
        
    try:
        data = datetime.strptime(data_referencia, "%Y-%m-%d")
        
        # Define o dia a ser usado (prioriza o dia base da matrícula, se fornecido)
        dia = dia_base if dia_base else data.day
        mes = data.month
        ano = data.year
        
        if periodo_plano == "trimestral":
            mes += 2
        elif periodo_plano == "semestral":
            mes +=5
        elif periodo_plano == "anual":
            ano +=1
        else: # mensal
            mes +=1
            
        # Ajusta o mês e ano se passar de 12
        while mes > 12:
            mes -= 12
            ano +=1
            
        # Tenta criar a data com o dia base, se falhar, vai diminuindo o dia até funcionar
        while True:
            try:
                nova_data = datetime(ano, mes, dia)
                break
            except ValueError:
                dia -=1
                if dia < 1:
                    dia = 31 # Reinicia para 31, mas o loop vai encontrar um dia válido
        
        return nova_data.strftime("%Y-%m-%d")
            
    except ValueError:
        return None


def salvar_cliente(nome, email, whatsapp, endereco, plano, valor_plano, data_matricula, data_vencimento, contato_emergencia, status, observacoes, idade=None, peso=None, altura=None, objetivo=None):
    # Limpa e converte o valor monetário
    valor_plano_convertido = limpar_valor_monetario(valor_plano)
    
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .insert({
            "nome": nome,
            "email": email,
            "whatsapp": whatsapp,
            "endereco": endereco,
            "plano": plano,
            "valor_plano": valor_plano_convertido,
            "periodo_plano": plano or "mensal",
            "data_matricula": data_matricula,
            "data_vencimento": data_vencimento,
            "contato_emergencia": contato_emergencia,
            "status": status,
            "observacoes": observacoes,
            "idade": idade,
            "peso": peso,
            "altura": altura,
            "objetivo": objetivo
        })
        .execute()
    )
    
    return result.data[0]["id"] if result.data else None


def buscar_clientes():
    supabase = get_supabase()
    # Primeiro busca só os clientes
    result = (
        supabase.table("clientes")
        .select("*")
        .order("nome")
        .execute()
    )
    
    clientes = []
    for cliente in result.data or []:
        cliente_dict = dict(cliente)
        cliente_dict["status"] = calcular_status_automatico(cliente_dict.get("data_vencimento"))
        
        # Busca o usuário relacionado separadamente
        if cliente_dict.get("id"):
            usuario_result = (
                supabase.table("usuarios")
                .select("activation_code, senha_hash")
                .eq("cliente_id", cliente_dict["id"])
                .limit(1)
                .execute()
            )
            if usuario_result.data:
                cliente_dict["activation_code"] = usuario_result.data[0].get("activation_code")
                cliente_dict["conta_ativa"] = 1 if usuario_result.data[0].get("senha_hash") else 0
            else:
                cliente_dict["activation_code"] = None
                cliente_dict["conta_ativa"] = 0
        else:
            cliente_dict["activation_code"] = None
            cliente_dict["conta_ativa"] = 0
            
        clientes.append(cliente_dict)
        
    return clientes


def buscar_cliente_por_id(id_cliente):
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .select("*")
        .eq("id", id_cliente)
        .execute()
    )
    
    if not result.data:
        return None
        
    cliente = dict(result.data[0])
    cliente["status"] = calcular_status_automatico(cliente.get("data_vencimento"))
    
    # Busca o usuário relacionado separadamente
    usuario_result = (
        supabase.table("usuarios")
        .select("activation_code, senha_hash")
        .eq("cliente_id", cliente["id"])
        .limit(1)
        .execute()
    )
    if usuario_result.data:
        cliente["activation_code"] = usuario_result.data[0].get("activation_code")
        cliente["conta_ativa"] = 1 if usuario_result.data[0].get("senha_hash") else 0
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


def atualizar_cliente(id_cliente, nome, email, whatsapp, endereco, plano, valor_plano, data_matricula, data_vencimento, contato_emergencia, status, observacoes, idade=None, peso=None, altura=None, objetivo=None):
    # Limpa e converte o valor monetário
    valor_plano_convertido = limpar_valor_monetario(valor_plano)
    
    supabase = get_supabase()
    result = (
        supabase.table("clientes")
        .update({
            "nome": nome,
            "email": email,
            "whatsapp": whatsapp,
            "endereco": endereco,
            "plano": plano,
            "valor_plano": valor_plano_convertido,
            "periodo_plano": plano or "mensal",
            "data_matricula": data_matricula,
            "data_vencimento": data_vencimento,
            "contato_emergencia": contato_emergencia,
            "status": status,
            "observacoes": observacoes,
            "idade": idade,
            "peso": peso,
            "altura": altura,
            "objetivo": objetivo
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
    print(f"pesquisar_clientes chamado com termo_pesquisa: '{termo_pesquisa}'")

    supabase = get_supabase()

    try:
        result = (
            supabase.table("clientes")
            .select("*")
            .or_(
                f"nome.ilike.%{termo_pesquisa}%,"
                f"email.ilike.%{termo_pesquisa}%,"
                f"whatsapp.ilike.%{termo_pesquisa}%,"
                f"endereco.ilike.%{termo_pesquisa}%,"
                f"plano.ilike.%{termo_pesquisa}%,"
                f"contato_emergencia.ilike.%{termo_pesquisa}%,"
                f"observacoes.ilike.%{termo_pesquisa}%"
            )
            .order("nome")
            .execute()
        )

        print("Resultado bruto:")
        print(result.data)
        print(f"Quantidade encontrada: {len(result.data) if result.data else 0}")

    except Exception as e:
        print(f"Erro na busca: {e}")
        return []

    clientes = []

    for cliente in result.data or []:
        cliente_dict = dict(cliente)

        cliente_dict["status"] = calcular_status_automatico(
            cliente_dict.get("data_vencimento")
        )

        cliente_dict["activation_code"] = None
        cliente_dict["conta_ativa"] = 0

        if cliente_dict.get("id"):
            try:
                usuario_result = (
                    supabase.table("usuarios")
                    .select("activation_code, senha_hash")
                    .eq("cliente_id", cliente_dict["id"])
                    .limit(1)
                    .execute()
                )

                if usuario_result.data:
                    cliente_dict["activation_code"] = usuario_result.data[0].get(
                        "activation_code"
                    )
                    cliente_dict["conta_ativa"] = (
                        1 if usuario_result.data[0].get("senha_hash") else 0
                    )

            except Exception as e:
                print(
                    f"Erro ao buscar usuário do cliente {cliente_dict['id']}: {e}"
                )

        clientes.append(cliente_dict)

    return clientes

def registrar_pagamento(id_cliente, valor_pagamento=None, data_pagamento=None, plano=None, data_vencimento_nova=None, tipo_pagamento="atual"):
    print(f"\n=== registrar_pagamento chamado ===")
    print(f"id_cliente: {id_cliente}")
    print(f"valor_pagamento: {valor_pagamento}")
    print(f"data_pagamento: {data_pagamento}")
    print(f"plano: {plano}")
    print(f"data_vencimento_nova: {data_vencimento_nova}")
    print(f"tipo_pagamento: {tipo_pagamento}")
    
    cliente = buscar_cliente_por_id(id_cliente)
    print(f"cliente encontrado: {cliente}")
    
    if not cliente:
        print("Cliente não encontrado!")
        return False
    
    # Usa os dados do cliente se não forem fornecidos
    data_vencimento_atual = cliente.get("data_vencimento")
    plano_usado = plano or cliente.get("plano", "mensal")
    valor_plano_convertido = limpar_valor_monetario(valor_pagamento) if valor_pagamento else cliente.get("valor_plano")
    data_pagamento_usada = data_pagamento or datetime.now().strftime("%Y-%m-%d")
    
    # Obtém o dia base da matrícula
    dia_base = None
    data_matricula = cliente.get("data_matricula")
    if data_matricula:
        try:
            dt_matricula = datetime.strptime(data_matricula, "%Y-%m-%d")
            dia_base = dt_matricula.day
        except Exception as e:
            print(f"Erro ao extrair dia da matrícula: {e}")
            dia_base = None
    
    print(f"data_vencimento_atual: {data_vencimento_atual}")
    print(f"plano_usado: {plano_usado}")
    print(f"valor_plano_convertido: {valor_plano_convertido}")
    print(f"data_pagamento_usada: {data_pagamento_usada}")
    print(f"dia_base (matrícula): {dia_base}")
    
    # Calcula nova data de vencimento
    if not data_vencimento_nova:
        print("Calculando nova data de vencimento...")
        if data_vencimento_atual:
            nova_data_vencimento = calcular_data_vencimento(data_vencimento_atual, plano_usado, dia_base)
            
            # Se for pagar tudo (inadimplente), calcula quantos meses estão atrasados
            if tipo_pagamento == "tudo":
                try:
                    data_venc = datetime.strptime(data_vencimento_atual, "%Y-%m-%d").date()
                    data_hoje = datetime.now().date()
                    dias_atraso = (data_hoje - data_venc).days
                    
                    if dias_atraso > 0:
                        # Calcula quantos meses de atraso (arredonda para cima)
                        meses_atraso = (dias_atraso + 30) // 30
                        print(f"Meses de atraso: {meses_atraso}")
                        
                        # Adiciona os meses atrasados
                        data_atual = data_venc
                        for _ in range(meses_atraso):
                            data_atual = datetime.strptime(calcular_data_vencimento(data_atual.strftime("%Y-%m-%d"), plano_usado, dia_base), "%Y-%m-%d").date()
                        # Adiciona o mês atual
                        nova_data_vencimento = calcular_data_vencimento(data_atual.strftime("%Y-%m-%d"), plano_usado, dia_base)
                except Exception as e:
                    print(f"Erro ao calcular pagamento total: {e}")
        else:
            nova_data_vencimento = calcular_data_vencimento(data_pagamento_usada, plano_usado, dia_base)
    else:
        nova_data_vencimento = data_vencimento_nova
        
    print(f"nova_data_vencimento: {nova_data_vencimento}")
        
    if nova_data_vencimento:
        supabase = get_supabase()
        # Prepara os dados para atualizar
        dados_atualizar = {
            "ultimo_pagamento": data_pagamento_usada,
            "data_vencimento": nova_data_vencimento,
            "status": "Pago",
            "plano": plano_usado,
            "periodo_plano": plano_usado
        }
        if valor_plano_convertido:
            dados_atualizar["valor_plano"] = valor_plano_convertido
            
        print(f"dados_atualizar: {dados_atualizar}")
            
        result = (
            supabase.table("clientes")
            .update(dados_atualizar)
            .eq("id", id_cliente)
            .execute()
        )
        
        print(f"result.data: {result.data}")
        print(f"len(result.data): {len(result.data)}")
        
        return len(result.data) > 0
    
    print("Nova data de vencimento é None, retornando False!")
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
