import os
import json
import requests
from backend.database.connection import get_supabase


def get_available_equipment():
    """Busca os equipamentos disponíveis na academia"""
    supabase = get_supabase()
    result = supabase.table("equipamentos").select("*").eq("disponivel", True).execute()
    return result.data or []


def generate_personalized_workout(client_data, num_dias, nivel_experiencia, tem_lesao, local_lesao=None):
    """
    Gera um treino personalizado usando IA (Ollama + Qwen)
    """
    # Busca equipamentos disponíveis
    equipamentos = get_available_equipment()
    equipamentos_nomes = [eq["nome"] for eq in equipamentos] if equipamentos else []

    # Prepara o prompt para a IA
    prompt = f"""
Você é um personal trainer experiente. Crie um treino personalizado para um aluno com as seguintes características:

Dados do Aluno:
- Nome: {client_data.get('nome', 'Aluno')}
- Idade: {client_data.get('idade', 'Não informado')} anos
- Peso: {client_data.get('peso', 'Não informado')} kg
- Altura: {client_data.get('altura', 'Não informado')} cm
- Nível de experiência: {nivel_experiencia}
- Tem lesão: {'Sim' if tem_lesao else 'Não'}
{f'- Local da lesão: {local_lesao}' if tem_lesao and local_lesao else ''}

Equipamentos disponíveis na academia:
{', '.join(equipamentos_nomes) if equipamentos_nomes else 'Equipamentos básicos (halteres, barras, colchonete)'}

Crie um treino de {num_dias} dias por semana.

Retorne o resultado EXCLUSIVAMENTE em formato JSON com a seguinte estrutura:
{{
  "dias": [
    {{
      "dia": 1,
      "nome": "Nome do Dia (ex: Peito e Tríceps)",
      "exercicios": [
        {{
          "nome": "Nome do Exercício",
          "series": 3,
          "repeticoes": "12-15",
          "equipamento": "Equipamento usado",
          "observacoes": "Dicas importantes"
        }}
      ]
    }}
  ]
}}

Não inclua nenhum texto adicional além do JSON.
"""

    # Configurações do Ollama
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
    ollama_model = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")

    try:
        # Requisição para o Ollama
        response = requests.post(
            ollama_url,
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7
                }
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        # Extrai e parseia o JSON
        content = result.get("response", "").strip()
        # Remove markdown se houver
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        workout_data = json.loads(content)
        return workout_data

    except Exception as e:
        print(f"Erro ao usar IA (Ollama): {e}")
        # Fallback para treino básico
        return generate_basic_workout(num_dias, nivel_experiencia, tem_lesao, local_lesao)


def generate_basic_workout(num_dias, nivel_experiencia, tem_lesao, local_lesao=None):
    """Gera um treino básico quando a IA não está disponível"""
    # Define séries e repetições
    if nivel_experiencia == "iniciante":
        series = 3
        repeticoes = "12-15"
    elif nivel_experiencia == "intermediario":
        series = 4
        repeticoes = "10-12"
    else:
        series = 4
        repeticoes = "8-10"

    # Exercícios básicos
    exercicios_basicos = [
        {"nome": "Agachamento", "equipamento": "Barra", "observacoes": "Mantenha a postura correta"},
        {"nome": "Supino", "equipamento": "Banco e barra", "observacoes": "Controle a descida"},
        {"nome": "Puxada Alta", "equipamento": "Máquina", "observacoes": "Mantenha os ombros afastados"},
        {"nome": "Rosca Direta", "equipamento": "Halteres", "observacoes": "Mantenha o cotovelo fixo"},
        {"nome": "Tríceps no Pulley", "equipamento": "Cabo", "observacoes": "Mantenha o core contraído"},
        {"nome": "Leg Press", "equipamento": "Máquina", "observacoes": "Não trave os joelhos"},
        {"nome": "Elevação Lateral", "equipamento": "Halteres", "observacoes": "Movimento controlado"},
        {"nome": "Cadeira Extensora", "equipamento": "Máquina", "observacoes": "Exala na extensão"}
    ]

    # Filtra exercícios se houver lesão
    exercicios_filtrados = []
    for ex in exercicios_basicos:
        if tem_lesao and local_lesao:
            lesao_low = local_lesao.lower()
            ex_nome_low = ex["nome"].lower()
            if lesao_low == "joelho" and ("agachamento" in ex_nome_low or "leg press" in ex_nome_low):
                continue
            if lesao_low == "ombro" and ("supino" in ex_nome_low or "elevação lateral" in ex_nome_low):
                continue
            if lesao_low == "lombar" and ("agachamento" in ex_nome_low):
                continue
        exercicios_filtrados.append(ex)

    if not exercicios_filtrados:
        exercicios_filtrados = exercicios_basicos

    # Cria treino
    dias = []
    nomes_dias = ["Peito e Tríceps", "Costas e Bíceps", "Pernas", "Ombros", "Full Body"]

    for i in range(num_dias):
        dia_exercicios = exercicios_filtrados[i::num_dias]
        if not dia_exercicios:
            dia_exercicios = exercicios_filtrados[:4]

        dias.append({
            "dia": i + 1,
            "nome": nomes_dias[i % len(nomes_dias)],
            "exercicios": [
                {**ex, "series": series, "repeticoes": repeticoes}
                for ex in dia_exercicios
            ]
        })

    return {"dias": dias}
