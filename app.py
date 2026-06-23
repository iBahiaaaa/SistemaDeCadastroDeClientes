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
    atualizar_cargo,
    pesquisar_funcionarios_controller
)
from backend.controllers.pagina_controller import (
    inicio,
    perfil
)
from backend.controllers.treino_controller import (
    pagina_treinos,
    gerar_treino,
    listar_treinos_cliente,
    pesquisar_treinos_route,
    listar_exercicios,
    adicionar_exercicio_treino,
    remover_exercicio_treino
)
from backend.controllers.equipamento_controller import (
    pagina_equipamentos,
    listar_equipamentos,
    criar_equipamento,
    atualizar_equipamento,
    excluir_equipamento
)
from backend.controllers.pagamento_controller import (
    pagina_pagamentos,
    pesquisar_pagamentos_controller
)
from backend.controllers.cliente_controller import (
    cadastrar_cliente,
    deletar_cliente,
    pesquisar_cliente_controller,
    registrar_pagamento_controller
)
from backend.services.auth_service import obter_primeiro_nome_para_header
from flask_swagger_ui import get_swaggerui_blueprint

from backend.utils.version import obter_versao

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Configuração do Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sistema de Cadastro de Clientes"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Adiciona rota para servir o arquivo swagger.json
def exempt_from_login(func):
    func._exempt_from_login = True
    return func

@app.route('/swagger.json')
@exempt_from_login
def serve_swagger_json():
    from flask import send_from_directory
    return send_from_directory('.', 'swagger.json')

app.before_request(exigir_login)

@app.context_processor
def inject_user():
    usuario_nome = obter_primeiro_nome_para_header(session)
    return dict(usuario_nome=usuario_nome)

@app.context_processor
def inject_version():
    return dict(app_version=obter_versao())

app.add_url_rule("/", view_func=inicio, methods=["GET"])
app.add_url_rule("/perfil", view_func=perfil, methods=["GET"])
app.add_url_rule("/funcionarios", view_func=pagina_funcionarios, methods=["GET"])
app.add_url_rule("/treinos", view_func=pagina_treinos, methods=["GET"])
app.add_url_rule("/treinos/gerar", view_func=gerar_treino, methods=["POST"])
app.add_url_rule("/treinos/cliente/<int:cliente_id>", view_func=listar_treinos_cliente, methods=["GET"])
app.add_url_rule("/pesquisar-treinos", view_func=pesquisar_treinos_route, methods=["GET"])
app.add_url_rule("/exercicios", view_func=listar_exercicios, methods=["GET"])
app.add_url_rule("/treinos/<int:treino_id>/exercicios", view_func=adicionar_exercicio_treino, methods=["POST"])
app.add_url_rule("/treinos/<int:treino_id>/exercicios/<int:exercicio_id>", view_func=remover_exercicio_treino, methods=["DELETE"])
app.add_url_rule("/pagamentos", view_func=pagina_pagamentos, methods=["GET"])
app.add_url_rule("/equipamentos", view_func=pagina_equipamentos, methods=["GET"])
app.add_url_rule("/api/equipamentos", view_func=listar_equipamentos, methods=["GET"])
app.add_url_rule("/api/equipamentos", view_func=criar_equipamento, methods=["POST"])
app.add_url_rule("/api/equipamentos/<int:id>", view_func=atualizar_equipamento, methods=["PUT"])
app.add_url_rule("/api/equipamentos/<int:id>", view_func=excluir_equipamento, methods=["DELETE"])

app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout, methods=["GET"])
app.add_url_rule("/ativar-conta", view_func=ativar_conta, methods=["GET", "POST"])

app.add_url_rule("/cadastrar", view_func=cadastrar_cliente, methods=["POST"])
app.add_url_rule("/excluir/<int:id_cliente>", view_func=deletar_cliente, methods=["POST"])
app.add_url_rule("/pesquisar", view_func=pesquisar_cliente_controller, methods=["GET"])
app.add_url_rule("/funcionarios/<int:id_usuario>/cargo", view_func=atualizar_cargo, methods=["POST"])
app.add_url_rule("/pesquisar-funcionarios", view_func=pesquisar_funcionarios_controller, methods=["GET"])
app.add_url_rule("/pesquisar-pagamentos", view_func=pesquisar_pagamentos_controller, methods=["GET"])
app.add_url_rule(
    "/registrar-pagamento/<int:id_cliente>",
    view_func=registrar_pagamento_controller,
    methods=["POST"]
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
