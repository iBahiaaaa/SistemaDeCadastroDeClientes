from flask import render_template, request, redirect, session, url_for

from backend.services.auth_service import autenticar, ativar_conta as ativar_conta_service


def login():
    if request.method == "GET":
        return render_template("login.html")

    resultado = autenticar(
        request.form.get("email"),
        request.form.get("senha")
    )

    if resultado["status"] == "erro":
        return render_template("login.html", erro=resultado["erro"])

    if resultado["status"] == "ativar":
        return redirect(url_for("ativar_conta", email=resultado.get("email")))

    session.update(resultado["session"])
    return redirect(url_for("inicio"))


def logout():
    session.clear()
    return redirect(url_for("login"))


def ativar_conta():
    if request.method == "GET":
        email = (request.args.get("email") or "").strip().lower()
        return render_template("ativar_conta.html", email=email)

    resultado = ativar_conta_service(
        request.form.get("email"),
        request.form.get("codigo"),
        request.form.get("senha"),
        request.form.get("confirmar_senha")
    )

    if resultado["status"] == "erro":
        return render_template(
            "ativar_conta.html",
            email=resultado.get("email"),
            erro=resultado.get("erro")
        )

    if resultado["status"] == "ja_ativo":
        return redirect(url_for("login"))

    return redirect(url_for("login"))
