from flask import Flask, render_template, request, redirect
from backend.controllers.cliente_controller import (
    cadastrar_cliente,
    listar_clientes,
    deletar_cliente
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

@app.template_filter('formatar_data')
def formatar_data(data_str):
    if not data_str or "-" not in data_str:
        return data_str
    try:
        partes = data_str.split("-")
        if len(partes) == 3:
            return f"{partes[2]}/{partes[1]}/{partes[0]}"
    except:
        return data_str
    return data_str

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    return cadastrar_cliente()

@app.route("/excluir/<int:id_cliente>", methods=["POST"])
def excluir(id_cliente):

    return deletar_cliente(id_cliente)
    
if __name__ == "__main__":
    app.run(host="25.0.103.60", port=5001, debug=True)