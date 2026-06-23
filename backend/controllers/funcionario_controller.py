from flask import render_template, request, redirect, url_for, jsonify

from backend.services.usuario_service import (
    listar_usuarios_com_exibicao,
    alterar_cargo_usuario
)
from backend.repositories.usuario_repository import pesquisar_usuarios


def pagina_funcionarios():
    mensagem = request.args.get("mensagem")
    erro = request.args.get("erro")

    return render_template(
        "funcionarios.html",
        usuarios=listar_usuarios_com_exibicao(),
        cargos=["ADM", "FUNCIONARIO", "INSTRUTOR", "FINANCEIRO", "ALUNO"],
        mensagem=mensagem,
        erro=erro
    )


def pesquisar_funcionarios_controller():
    termo = request.args.get('termo', '')
    usuarios = pesquisar_usuarios(termo)
    
    # Aplicar a mesma lógica de exibição que listar_usuarios_com_exibicao
    from backend.repositories.cliente_repository import (
        buscar_nome_cliente_por_id,
        buscar_cliente_por_email
    )
    
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
    
    return jsonify(usuarios)


def atualizar_cargo(id_usuario):
    resultado = alterar_cargo_usuario(id_usuario, request.form.get("cargo"))

    if not resultado["ok"]:
        return redirect(url_for("pagina_funcionarios", erro=resultado["erro"]))

    return redirect(url_for("pagina_funcionarios", mensagem="Cargo atualizado com sucesso."))
