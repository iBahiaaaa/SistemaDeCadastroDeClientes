from flask import request, jsonify
from backend.repositories.treino_repository import (
    criar_treino,
    buscar_treinos_por_cliente,
    buscar_treino_por_id
)
from backend.repositories.cliente_repository import buscar_cliente_por_id

def gerar_treino():
    data = request.get_json() or request.form
    cliente_id = data.get("cliente_id")
    nivel_experiencia = data.get("nivel_experiencia")
    tem_lesao = data.get("tem_lesao", "false").lower() == "true"
    local_lesao = data.get("local_lesao") if tem_lesao else None
    
    if not cliente_id or not nivel_experiencia:
        return jsonify({"erro": "Cliente e nível de experiência são obrigatórios"}), 400
    
    # Verifica se o cliente existe
    cliente = buscar_cliente_por_id(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    
    # Cria o treino
    treino = criar_treino(cliente_id, nivel_experiencia, tem_lesao, local_lesao)
    
    if not treino:
        return jsonify({"erro": "Não foi possível gerar o treino"}), 500
    
    return jsonify(treino), 201

def listar_treinos_cliente(cliente_id):
    cliente = buscar_cliente_por_id(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    
    treinos = buscar_treinos_por_cliente(cliente_id)
    return jsonify(treinos)
