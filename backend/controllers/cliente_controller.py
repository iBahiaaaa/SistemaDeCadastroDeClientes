from flask import request, redirect
from flask import request, redirect
from backend.repositories.cliente_repository import (
    salvar_cliente,
    buscar_clientes,
    excluir_cliente,
    atualizar_cliente
)


def cadastrar_cliente():

    nome = request.form["nome"]
    whatsapp = request.form["whatsapp"]
    endereco = request.form["endereco"]
    observacoes = request.form["observacoes"]

    salvar_cliente(
        nome,
        whatsapp,
        endereco,
        observacoes
    )

    return redirect("/")

def listar_clientes():

    clientes = buscar_clientes()

    return clientes

def deletar_cliente(id_cliente):

    excluir_cliente(id_cliente)

    return redirect("/")

def cadastrar_cliente():

    id_cliente = request.form.get("id_cliente")

    nome = request.form["nome"]
    whatsapp = request.form["whatsapp"]
    endereco = request.form["endereco"]
    observacoes = request.form["observacoes"]

    if id_cliente:
        atualizar_cliente(id_cliente, nome, whatsapp, endereco, observacoes)
    else:
        salvar_cliente(nome, whatsapp, endereco, observacoes)

    return redirect("/")