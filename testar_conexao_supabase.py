from backend.database.connection import get_supabase

print("Testando conexão com o Supabase...")
try:
    supabase = get_supabase()
    print("✓ Conexão com o Supabase estabelecida com sucesso!")
    
    # Tenta fazer uma consulta simples para verificar
    result = supabase.table("usuarios").select("count", count="exact").execute()
    print(f"✓ Número de usuários na tabela: {result.count}")
    
    print("\n✓ Conexão está funcionando perfeitamente!")
    
except Exception as e:
    print(f"✗ Erro ao conectar com o Supabase: {e}")
