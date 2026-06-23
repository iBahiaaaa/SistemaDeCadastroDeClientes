from flask import render_template, request, jsonify
from backend.repositories.cliente_repository import buscar_clientes, pesquisar_clientes, calcular_status_automatico

def pagina_pagamentos():
    # Obtém todos os clientes e converte para o formato de pagamentos
    clientes = buscar_clientes()
    pagamentos = []
    
    for cliente in clientes:
        pagamentos.append({
            "id": cliente["id"],
            "cliente_id": cliente["id"],
            "cliente_nome": cliente["nome"],
            "valor": cliente.get("valor_plano", 0),
            "data": cliente.get("ultimo_pagamento"),
            "plano": cliente.get("plano", "mensal"),
            "status": cliente["status"],
            "data_vencimento": cliente.get("data_vencimento"),
            "ultimo_pagamento": cliente.get("ultimo_pagamento")
        })
    
    return render_template("pagamentos.html", pagamentos=pagamentos)

def pesquisar_pagamentos_controller():
    termo = request.args.get("termo", "")
    clientes = pesquisar_clientes(termo)
    
    pagamentos = []
    for cliente in clientes:
        pagamentos.append({
            "id": cliente["id"],
            "cliente_id": cliente["id"],
            "cliente_nome": cliente["nome"],
            "valor": cliente.get("valor_plano", 0),
            "data": cliente.get("ultimo_pagamento"),
            "plano": cliente.get("plano", "mensal"),
            "status": cliente["status"],
            "data_vencimento": cliente.get("data_vencimento"),
            "ultimo_pagamento": cliente.get("ultimo_pagamento")
        })
    
    return jsonify(pagamentos)
