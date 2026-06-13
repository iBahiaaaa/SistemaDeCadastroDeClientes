from backend.repositories.usuario_repository import buscar_usuario_por_email
from werkzeug.security import check_password_hash

print("Testando busca de usuário...")
email_teste = "vinioa1998@gmail.com"
usuario = buscar_usuario_por_email(email_teste)

print(f"Resultado da busca: {usuario}")

if usuario:
    print(f"ID: {usuario.get('id')}")
    print(f"Email: {usuario.get('email')}")
    print(f"Senha hash: {usuario.get('senha_hash')}")
    print(f"Cargo: {usuario.get('cargo')}")
    
    # Testa a senha
    senha_teste = "vineira123"
    if check_password_hash(usuario.get('senha_hash'), senha_teste):
        print("✓ Senha correta!")
    else:
        print("✗ Senha incorreta!")
else:
    print("Usuário não encontrado!")
