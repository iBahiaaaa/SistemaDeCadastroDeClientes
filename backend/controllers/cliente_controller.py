from flask import request, redirect

from backend.repositories.cliente_repository import (
    salvar_cliente,
    buscar_clientes,
    excluir_cliente,
    atualizar_cliente
)


def cadastrar_cliente():

    id_cliente = request.form.get("id_cliente")

    nome = request.form.get("nome", "").strip()
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

    if id_cliente:
        atualizar_cliente(
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
        )
    else:
        salvar_cliente(
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

    return redirect("/")


def listar_clientes():
    return buscar_clientes() or []


def deletar_cliente(id_cliente):
    excluir_cliente(id_cliente)
    return redirect("/")