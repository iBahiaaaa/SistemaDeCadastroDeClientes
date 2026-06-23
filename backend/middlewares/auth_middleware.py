from flask import request, redirect, session, url_for


def exigir_login():
    # Rotas que não precisam de login
    rotas_livres = ["/static", "/login", "/logout", "/ativar-conta", "/swagger", "/swagger.json"]
    for rota in rotas_livres:
        if request.path.startswith(rota):
            return None

    if not session.get("usuario_id"):
        return redirect(url_for("login"))

    return None
