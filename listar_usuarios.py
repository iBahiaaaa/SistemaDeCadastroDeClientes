from backend.database.connection import get_supabase

print("Listando todos os usuários do Supabase...")
supabase = get_supabase()
result = supabase.table("usuarios").select("*").execute()

print(f"Resultado: {result}")

if result.data:
    print(f"Total de usuários: {len(result.data)}")
    for i, user in enumerate(result.data):
        print(f"Usuário {i+1}:")
        print(f"  ID: {user.get('id')}")
        print(f"  Nome: {user.get('nome')}")
        print(f"  Email: {user.get('email')}")
        print(f"  Cargo: {user.get('cargo')}")
else:
    print("Nenhum usuário encontrado na tabela!")
