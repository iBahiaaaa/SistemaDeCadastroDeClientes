from backend.database.connection import get_supabase

CARGOS_VALIDOS = ("ADM", "FUNCIONARIO", "INSTRUTOR", "FINANCEIRO", "ALUNO")


def buscar_usuario_por_email(email):
    if not email:
        return None

    supabase = get_supabase()
    result = (
        supabase.table("usuarios")
        .select("id, nome, email, senha_hash, cargo, cliente_id, activation_code, activation_created_at")
        .ilike("email", email.strip().lower())
        .limit(1)
        .execute()
    )
    
    return result.data[0] if result.data else None


def definir_senha_hash(id_usuario, senha_hash):
    supabase = get_supabase()
    result = (
        supabase.table("usuarios")
        .update({
            "senha_hash": senha_hash,
            "activation_code": None,
            "activation_created_at": None
        })
        .eq("id", id_usuario)
        .execute()
    )
    
    return len(result.data) > 0


def listar_usuarios():
    supabase = get_supabase()
    result = (
        supabase.table("usuarios")
        .select("id, nome, email, cargo, cliente_id")
        .order("nome", nullsfirst=False)
        .execute()
    )
    
    # Se o nome for nulo, ordena por email
    users = result.data or []
    users.sort(key=lambda u: (u.get("nome") is None, u.get("nome") or u.get("email")))
    
    return users


def atualizar_cargo_usuario(id_usuario, cargo):
    supabase = get_supabase()
    result = (
        supabase.table("usuarios")
        .update({"cargo": cargo})
        .eq("id", id_usuario)
        .execute()
    )
    
    return len(result.data) > 0
