import sqlite3
from flask import Flask, render_template, request, redirect
from backend.controllers.cliente_controller import (
    cadastrar_cliente,
    listar_clientes
)

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

@app.route("/")
def inicio():

    clientes = listar_clientes()

    return render_template(
        "clientes.html",
        clientes=clientes
    )

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    return cadastrar_cliente()
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)