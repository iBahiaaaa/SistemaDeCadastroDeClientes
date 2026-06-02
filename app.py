import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)
@app.route("/")
def inicio():

    conexao = sqlite3.connect("backend/database/banco.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    conexao.close()

    return render_template("clientes.html", clientes=clientes)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    whatsapp = request.form["whatsapp"] 
    endereco = request.form["endereco"]
    observacoes = request.form["observacoes"]

    conexao = sqlite3.connect("backend/database/banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nome, whatsapp, endereco, observacoes)
        VALUES (?, ?, ?, ?)
    """, (nome, whatsapp, endereco, observacoes))

    conexao.commit()
    conexao.close()

    return redirect("/")
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)