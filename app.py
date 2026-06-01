import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("clientes.html")

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    whatsapp = request.form["whatsapp"]
    endereco = request.form["endereco"]
    observacoes = request.form["observacoes"]

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nome, whatsapp, endereco, observacoes)
        VALUES (?, ?, ?, ?)
    """, (nome, whatsapp, endereco, observacoes))

    conexao.commit()
    conexao.close()

    return "Cliente cadastrado com sucesso!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)