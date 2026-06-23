from flask import request, jsonify, render_template
from backend.repositories.equipamento_repository import (
    get_all_equipamentos,
    add_equipamento,
    update_equipamento,
    delete_equipamento
)


def pagina_equipamentos():
    equipamentos = get_all_equipamentos()
    return render_template("equipamentos.html", equipamentos=equipamentos)


def listar_equipamentos():
    equipamentos = get_all_equipamentos()
    return jsonify(equipamentos)


def criar_equipamento():
    data = request.get_json() or request.form
    nome = data.get("nome")
    disponivel = data.get("disponivel", True)
    if not nome:
        return jsonify({"erro": "Nome do equipamento é obrigatório"}), 400
    equipamento = add_equipamento(nome, disponivel)
    return jsonify(equipamento), 201


def atualizar_equipamento(id):
    data = request.get_json() or request.form
    nome = data.get("nome")
    disponivel = data.get("disponivel")
    disponivel_bool = None
    if disponivel is not None:
        disponivel_bool = str(disponivel).lower() in ["true", "1", "yes"]
    sucesso = update_equipamento(id, nome, disponivel_bool)
    if sucesso:
        return jsonify({"sucesso": True})
    return jsonify({"erro": "Equipamento não encontrado"}), 404


def excluir_equipamento(id):
    sucesso = delete_equipamento(id)
    if sucesso:
        return jsonify({"sucesso": True})
    return jsonify({"erro": "Equipamento não encontrado"}), 404
