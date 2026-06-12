from flask import request, redirect, jsonify

from backend.repositories.cliente_repository import (
    salvar_cliente,
    buscar_clientes,
    excluir_cliente,
    atualizar_cliente,
    pesquisar_clientes,
    registrar_pagamento,
    email_em_uso_em_outro_cliente,
    email_em_uso_em_usuario,
    garantir_conta_aluno
)


def cadastrar_cliente():

    id_cliente = request.form.get("id_cliente")

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    whatsapp = request.form.get("whatsapp", "").strip()
    endereco = request.form.get("endereco", "").strip()
    plano = request.form.get("plano")
    valor_plano = request.form.get("valor_plano")
    data_matricula = request.form.get("data_matricula")
    data_vencimento = request.form.get("data_vencimento")
    contato_emergencia = request.form.get("contato_emergencia")
    status = request.form.get("status")
    observacoes = request.form.get("observacoes", "").strip()

    if not nome:
        return "Nome é obrigatório", 400

    if email:
        if email_em_uso_em_outro_cliente(email, id_cliente=int(id_cliente) if id_cliente else None):
            return "Esse email já está vinculado a outro cliente.", 400

        if email_em_uso_em_usuario(email, cliente_id=int(id_cliente) if id_cliente else None):
            return "Esse email já está em uso no sistema.", 400

    if id_cliente:
        ok = atualizar_cliente(
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
        )
        if email:
            garantir = garantir_conta_aluno(int(id_cliente), email)
            if garantir is None:
                return "Não foi possível vincular a conta desse aluno (email em uso).", 400
    else:
        novo_id = salvar_cliente(
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
        if not novo_id:
            return "Erro ao salvar cliente.", 500
        if email:
            garantir = garantir_conta_aluno(int(novo_id), email)
            if garantir is None:
                return "Não foi possível vincular a conta desse aluno (email em uso).", 400

    return redirect("/")


def registrar_pagamento_controller(id_cliente):
    sucesso = registrar_pagamento(id_cliente)
    return redirect("/")


def listar_clientes():
    return buscar_clientes() or []


def deletar_cliente(id_cliente):
    excluir_cliente(id_cliente)
    return redirect("/")


def pesquisar_cliente_controller():
    termo = request.args.get('termo', '')
    clientes = pesquisar_clientes(termo)
    return jsonify(clientes)
