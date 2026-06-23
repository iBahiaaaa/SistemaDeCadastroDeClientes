from flask import render_template

from backend.controllers.cliente_controller import listar_clientes


def inicio():
    clientes = listar_clientes()
    return render_template("clientes.html", clientes=clientes)


def perfil():
    return "Em desenvolvimento", 200


def pagina_treinos():
    return render_template("treinos.html")
