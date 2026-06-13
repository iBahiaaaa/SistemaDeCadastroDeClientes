from werkzeug.security import generate_password_hash

# Dados do usuário admin
email = "vinioa1998@gmail.com"
senha = "vineira123"
cargo = "ADM"
nome = "Vinícius"

# Gera o hash da senha
senha_hash = generate_password_hash(senha)

# SQL para inserir o usuário no Supabase
sql = f"""
INSERT INTO usuarios (nome, email, senha_hash, cargo)
VALUES ('{nome}', '{email}', '{senha_hash}', '{cargo}');
"""

print("Senha hash gerada:")
print(senha_hash)
print("\nSQL para inserir no Supabase:")
print(sql)
