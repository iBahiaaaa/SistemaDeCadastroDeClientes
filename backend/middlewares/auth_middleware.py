from flask import request, redirect, session, url_for


def exigir_login():
    if request.path.startswith("/static/"):
        return None

    endpoints_livres = {"login", "ativar_conta", "logout", "static"}
    if request.endpoint in endpoints_livres:
        return None

    if not session.get("usuario_id"):
        return redirect(url_for("login"))

    return None
