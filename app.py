import os
from dotenv import load_dotenv

from flask import Flask

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
    perfil
)
from backend.controllers.cliente_controller import (
    cadastrar_cliente,
    deletar_cliente,
    pesquisar_cliente_controller,
    registrar_pagamento_controller
)

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.before_request(exigir_login)

app.add_url_rule("/", view_func=inicio, methods=["GET"])
app.add_url_rule("/perfil", view_func=perfil, methods=["GET"])
app.add_url_rule("/funcionarios", view_func=pagina_funcionarios, methods=["GET"])

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
    app.run(host="25.0.103.60", port=5001, debug=True)
