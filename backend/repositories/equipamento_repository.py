from backend.database.connection import get_supabase


def get_all_equipamentos():
    """Busca todos os equipamentos"""
    supabase = get_supabase()
    result = supabase.table("equipamentos").select("*").order("nome").execute()
    return result.data or []


def add_equipamento(nome, disponivel=True):
    """Adiciona um novo equipamento"""
    supabase = get_supabase()
    result = supabase.table("equipamentos").insert({
        "nome": nome,
        "disponivel": disponivel
    }).execute()
    return result.data[0] if result.data else None


def update_equipamento(id, nome=None, disponivel=None):
    """Atualiza um equipamento"""
    supabase = get_supabase()
    data = {}
    if nome is not None:
        data["nome"] = nome
    if disponivel is not None:
        data["disponivel"] = disponivel
    result = supabase.table("equipamentos").update(data).eq("id", id).execute()
    return len(result.data) > 0


def delete_equipamento(id):
    """Exclui um equipamento"""
    supabase = get_supabase()
    result = supabase.table("equipamentos").delete().eq("id", id).execute()
    return len(result.data) > 0
