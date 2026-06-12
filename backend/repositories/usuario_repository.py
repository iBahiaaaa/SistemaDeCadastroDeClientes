from backend.database.connection import execute_query

CARGOS_VALIDOS = ("ADM", "FUNCIONARIO", "INSTRUTOR", "FINANCEIRO", "ALUNO")


def buscar_usuario_por_email(email):
    if not email:
        return None

    resultado = execute_query(
        """
        SELECT
            id,
            nome,
            email,
            senha_hash,
            cargo,
            cliente_id,
            activation_code,
            activation_created_at
        FROM usuarios
        WHERE LOWER(email) = ?
        LIMIT 1
        """,
        (email.strip().lower(),),
        is_select=True
    )
    if not resultado:
        return None
    return dict(resultado[0])


def definir_senha_hash(id_usuario, senha_hash):
    return execute_query(
        "UPDATE usuarios SET senha_hash = ?, activation_code = NULL, activation_created_at = NULL WHERE id = ?",
        (senha_hash, id_usuario)
    )


def listar_usuarios():
    resultado = execute_query(
        """
        SELECT
            id,
            nome,
            email,
            cargo,
            cliente_id
        FROM usuarios
        ORDER BY
            CASE
                WHEN nome IS NULL OR TRIM(nome) = '' THEN email
                ELSE nome
            END
        """,
        is_select=True
    ) or []
    return [dict(usuario) for usuario in resultado]


def atualizar_cargo_usuario(id_usuario, cargo):
    return execute_query(
        "UPDATE usuarios SET cargo = ? WHERE id = ?",
        (cargo, id_usuario)
    )
