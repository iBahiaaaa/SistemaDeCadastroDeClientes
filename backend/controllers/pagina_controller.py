from flask import render_template, session

from backend.controllers.cliente_controller import listar_clientes
from backend.services.auth_service import obter_primeiro_nome_para_header


def inicio():
    clientes = listar_clientes()
    usuario_nome = obter_primeiro_nome_para_header(session)
    return render_template("clientes.html", clientes=clientes, usuario_nome=usuario_nome)


def perfil():
    return "Em desenvolvimento", 200
