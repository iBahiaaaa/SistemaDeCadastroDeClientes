import os
from dotenv import load_dotenv

from flask import Flask, session

from backend.middlewares.auth_middleware import exigir_login
from backend.controllers.auth_controller import (
    login,
    logout,
    ativar_conta
)
from backend.controllers.funcionario_controller import (
    pagina_funcionarios,
    atualizar_cargo
)
from backend.controllers.pagina_controller import (
    inicio,
    perfil,
    pagina_treinos
)
from backend.controllers.cliente_controller import (
    cadastrar_cliente,
    deletar_cliente,
    pesquisar_cliente_controller,
    registrar_pagamento_controller
)
from backend.services.auth_service import obter_primeiro_nome_para_header

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.before_request(exigir_login)

@app.context_processor
def inject_user():
    usuario_nome = obter_primeiro_nome_para_header(session)
    return dict(usuario_nome=usuario_nome)

app.add_url_rule("/", view_func=inicio, methods=["GET"])
app.add_url_rule("/perfil", view_func=perfil, methods=["GET"])
app.add_url_rule("/funcionarios", view_func=pagina_funcionarios, methods=["GET"])
app.add_url_rule("/treinos", view_func=pagina_treinos, methods=["GET"])

app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout, methods=["GET"])
app.add_url_rule("/ativar-conta", view_func=ativar_conta, methods=["GET", "POST"])

app.add_url_rule("/cadastrar", view_func=cadastrar_cliente, methods=["POST"])
app.add_url_rule("/excluir/<int:id_cliente>", view_func=deletar_cliente, methods=["POST"])
app.add_url_rule("/pesquisar", view_func=pesquisar_cliente_controller, methods=["GET"])
app.add_url_rule("/funcionarios/<int:id_usuario>/cargo", view_func=atualizar_cargo, methods=["POST"])
app.add_url_rule(
    "/registrar-pagamento/<int:id_cliente>",
    view_func=registrar_pagamento_controller,
    methods=["POST"]
)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
