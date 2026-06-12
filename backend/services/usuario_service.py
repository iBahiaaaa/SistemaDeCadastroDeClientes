from backend.repositories.usuario_repository import (
    CARGOS_VALIDOS,
    listar_usuarios,
    atualizar_cargo_usuario
)
from backend.repositories.cliente_repository import (
    buscar_nome_cliente_por_id,
    buscar_cliente_por_email
)


def listar_usuarios_com_exibicao():
    usuarios = listar_usuarios()

    for usuario in usuarios:
        nome = (usuario.get("nome") or "").strip()
        email = (usuario.get("email") or "").strip()
        if not nome and usuario.get("cliente_id"):
            nome = (buscar_nome_cliente_por_id(usuario.get("cliente_id")) or "").strip()

        if not nome and email:
            cliente = buscar_cliente_por_email(email)
            if cliente:
                nome = (cliente.get("nome") or "").strip()

        usuario["nome_exibicao"] = nome or email.split("@")[0]
        usuario["possui_vinculo_cliente"] = bool(usuario.get("cliente_id"))

    return usuarios


def alterar_cargo_usuario(id_usuario, cargo):
    cargo = (cargo or "").strip().upper()

    if cargo not in CARGOS_VALIDOS:
        return {"ok": False, "erro": "Cargo inválido."}

    ok = atualizar_cargo_usuario(id_usuario, cargo)
    if not ok:
        return {"ok": False, "erro": "Não foi possível atualizar o cargo."}

    return {"ok": True}
