from flask import render_template, request, redirect, url_for

from backend.services.usuario_service import (
    listar_usuarios_com_exibicao,
    alterar_cargo_usuario
)


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


def atualizar_cargo(id_usuario):
    resultado = alterar_cargo_usuario(id_usuario, request.form.get("cargo"))

    if not resultado["ok"]:
        return redirect(url_for("pagina_funcionarios", erro=resultado["erro"]))

    return redirect(url_for("pagina_funcionarios", mensagem="Cargo atualizado com sucesso."))
