from flask import request, jsonify, render_template
from backend.repositories.treino_repository import (
    criar_treino,
    buscar_treinos_por_cliente,
    buscar_treino_por_id
)
from backend.repositories.cliente_repository import (
    buscar_cliente_por_id,
    buscar_clientes,
    pesquisar_clientes
)

def pagina_treinos():
    clientes = buscar_clientes()
    return render_template("treinos.html", clientes=clientes)

def pesquisar_treinos_route():
    termo = request.args.get("termo", "")
    clientes = pesquisar_clientes(termo)
    return jsonify(clientes)

def gerar_treino():
    data = request.get_json() or request.form
    cliente_id = data.get("cliente_id")
    nivel_experiencia = data.get("nivel_experiencia")
    num_dias = int(data.get("numDias", 3))
    tem_lesao = data.get("tem_lesao", "false").lower() == "true"
    local_lesao = data.get("local_lesao") if tem_lesao else None
    
    if not cliente_id or not nivel_experiencia:
        return jsonify({"erro": "Cliente e nível de experiência são obrigatórios"}), 400
    
    # Verifica se o cliente existe
    cliente = buscar_cliente_por_id(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    
    # Cria o treino
    treino = criar_treino(cliente_id, nivel_experiencia, tem_lesao, local_lesao, num_dias)
    
    if not treino:
        return jsonify({"erro": "Não foi possível gerar o treino"}), 500
    
    return jsonify(treino), 201

def listar_treinos_cliente(cliente_id):
    cliente = buscar_cliente_por_id(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    
    treinos = buscar_treinos_por_cliente(cliente_id)
    return jsonify(treinos)

def listar_exercicios():
    from backend.repositories.treino_repository import get_supabase
    supabase = get_supabase()
    exercicios = supabase.table("exercicios").select("*").execute().data
    return jsonify(exercicios)

def adicionar_exercicio_treino(treino_id):
    from backend.repositories.treino_repository import get_supabase, buscar_treino_por_id
    data = request.get_json()
    exercicio_id = data.get("exercicio_id")
    dia = int(data.get("dia", 1))
    series = int(data.get("series", 3))
    repeticoes = data.get("repeticoes", "12-15")
    
    if not exercicio_id:
        return jsonify({"erro": "Exercício obrigatório"}), 400
    
    treino = buscar_treino_por_id(treino_id)
    if not treino:
        return jsonify({"erro": "Treino não encontrado"}), 404
    
    supabase = get_supabase()
    
    # Get max ordem
    max_ordem = 0
    relacoes = supabase.table("treino_exercicios").select("ordem").eq("treino_id", treino_id).execute().data
    if relacoes:
        max_ordem = max(r["ordem"] for r in relacoes)
    
    # Add new exercicio
    result = supabase.table("treino_exercicios").insert({
        "treino_id": treino_id,
        "exercicio_id": exercicio_id,
        "dia": dia,
        "series": series,
        "repeticoes": repeticoes,
        "ordem": max_ordem + 1
    }).execute()
    
    if not result.data:
        return jsonify({"erro": "Não foi possível adicionar exercício"}), 500
    
    return jsonify({"sucesso": True}), 201

def remover_exercicio_treino(treino_id, exercicio_id):
    from backend.repositories.treino_repository import get_supabase, buscar_treino_por_id
    treino = buscar_treino_por_id(treino_id)
    if not treino:
        return jsonify({"erro": "Treino não encontrado"}), 404
    
    supabase = get_supabase()
    result = supabase.table("treino_exercicios").delete().eq("treino_id", treino_id).eq("exercicio_id", exercicio_id).execute()
    
    if not result.data:
        return jsonify({"erro": "Não foi possível remover exercício"}), 500
    
    return jsonify({"sucesso": True}), 200
