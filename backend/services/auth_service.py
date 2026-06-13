from werkzeug.security import check_password_hash, generate_password_hash

from backend.repositories.cliente_repository import (
    buscar_cliente_por_email,
    buscar_nome_cliente_por_id
)
from backend.repositories.usuario_repository import (
    buscar_usuario_por_email,
    definir_senha_hash
)


def autenticar(email, senha):
    email = (email or "").strip().lower()
    senha = senha or ""

    if not email:
        return {"status": "erro", "erro": "Preencha o email."}

    usuario = buscar_usuario_por_email(email)
    if not usuario:
        return {"status": "erro", "erro": "Email ou senha inválidos."}

    if not usuario.get("senha_hash"):
        return {"status": "ativar", "email": email}

    if not senha:
        return {"status": "erro", "erro": "Digite a senha."}

    if not check_password_hash(usuario["senha_hash"], senha):
        return {"status": "erro", "erro": "Email ou senha inválidos."}

    cliente_id = usuario.get("cliente_id")
    if not cliente_id:
        cliente = buscar_cliente_por_email(usuario.get("email"))
        if cliente:
            cliente_id = cliente.get("id")

    return {
        "status": "ok",
        "session": {
            "usuario_id": usuario["id"],
            "usuario_email": usuario["email"],
            "usuario_cargo": usuario["cargo"],
            "usuario_nome": usuario.get("nome"),
            "cliente_id": cliente_id
        }
    }


def ativar_conta(email, codigo, senha, confirmar_senha):
    email = (email or "").strip().lower()
    codigo = (codigo or "").strip()
    senha = senha or ""
    confirmar_senha = confirmar_senha or ""

    if not email or not codigo or not senha or not confirmar_senha:
        return {"status": "erro", "erro": "Preencha todos os campos.", "email": email}

    if senha != confirmar_senha:
        return {"status": "erro", "erro": "As senhas não conferem.", "email": email}

    usuario = buscar_usuario_por_email(email)
    if not usuario:
        return {"status": "erro", "erro": "Email ou senha inválidos.", "email": email}

    if usuario.get("senha_hash"):
        return {"status": "ja_ativo"}

    if not usuario.get("activation_code") or usuario["activation_code"] != codigo:
        return {"status": "erro", "erro": "Código inválido.", "email": email}

    senha_hash = generate_password_hash(senha)
    ok = definir_senha_hash(usuario["id"], senha_hash)
    if not ok:
        return {"status": "erro", "erro": "Não foi possível ativar a conta.", "email": email}

    return {"status": "ok"}


def obter_primeiro_nome_para_header(session):
    nome_base = (session.get("usuario_nome") or "").strip()

    if not nome_base and session.get("cliente_id"):
        nome_cliente = buscar_nome_cliente_por_id(session.get("cliente_id"))
        if nome_cliente:
            nome_base = nome_cliente

    if not nome_base and session.get("usuario_email"):
        cliente = buscar_cliente_por_email(session.get("usuario_email"))
        if cliente and cliente.get("nome"):
            nome_base = cliente.get("nome")

    if not nome_base and session.get("usuario_email"):
        nome_base = session.get("usuario_email").split("@")[0]

    return (nome_base.split() or ["Usuário"])[0]
