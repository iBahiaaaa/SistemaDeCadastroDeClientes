from backend.database.connection import get_supabase
from werkzeug.security import generate_password_hash

print("Inserindo usuário admin...")

# Dados do admin
nome = "Vinícius"
email = "vinioa1998@gmail.com"
senha = "vineira123"
cargo = "ADM"

# Gera hash da senha
senha_hash = generate_password_hash(senha)
print(f"Senha hash: {senha_hash}")

# Conecta ao Supabase
supabase = get_supabase()

# Verifica se o usuário já existe
result = supabase.table("usuarios").select("*").ilike("email", email).limit(1).execute()
if result.data:
    print("Usuário já existe! Atualizando senha...")
    update_result = (
        supabase.table("usuarios")
        .update({"senha_hash": senha_hash, "cargo": cargo, "nome": nome})
        .eq("email", email)
        .execute()
    )
    print(f"Atualização: {update_result}")
else:
    print("Criando novo usuário...")
    insert_result = (
        supabase.table("usuarios")
        .insert({
            "nome": nome,
            "email": email,
            "senha_hash": senha_hash,
            "cargo": cargo
        })
        .execute()
    )
    print(f"Inserção: {insert_result}")

print("✓ Pronto!")
