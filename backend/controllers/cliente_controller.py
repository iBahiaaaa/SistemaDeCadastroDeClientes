from flask import request, redirect
from flask import request, redirect
from backend.repositories.cliente_repository import (
    salvar_cliente,
    buscar_clientes
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