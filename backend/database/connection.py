import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.environ.get("https://uwjcimdpdnlriquuzreo.supabase.co")
SUPABASE_KEY = os.environ.get("sb_publishable_QLzB0eIRDWULsDzvPooO_A_We6GqI_h")

def get_supabase() -> Client:
    """
    Retorna uma instância do cliente Supabase.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise Exception("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY são necessárias")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def execute_query(query, params=(), is_select=False, return_lastrowid=False):
    """
    Essa função existe para manter a compatibilidade com o código antigo.
    Vamos atualizar todas as chamadas para usar diretamente o cliente Supabase nos repositórios.
    """
    print("Aviso: execute_query está deprecated. Use get_supabase() diretamente.")
    return None
