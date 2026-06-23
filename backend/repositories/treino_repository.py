from backend.database.connection import get_supabase
from backend.services.ai_workout_service import generate_personalized_workout

def buscar_exercicios(nivel_experiencia, local_lesao=None):
    """
    Busca exercícios adequados com base no nível de experiência e lesão (se houver)
    """
    supabase = get_supabase()
    query = (
        supabase.table("exercicios")
        .select("*")
        .eq("nivel_experiencia", nivel_experiencia)
    )

    result = query.execute()
    exercicios = []

    for exercicio in result.data or []:
        # Verifica se o exercício tem restrições para a lesão do cliente
        restricoes = exercicio.get("restricoes_lesao", "")
        if local_lesao and restricoes:
            restricoes_lista = [r.strip().lower() for r in restricoes.split(",")]
            if local_lesao.lower() in restricoes_lista:
                continue  # Pula esse exercício por causa da lesão
        exercicios.append(exercicio)

    return exercicios

def criar_treino(cliente_id, nivel_experiencia, tem_lesao, local_lesao=None, num_dias=3):
    """
    Cria um novo treino para o cliente usando IA
    """
    supabase = get_supabase()

    # Busca dados do cliente
    cliente_result = supabase.table("clientes").select("*").eq("id", cliente_id).execute()
    cliente = cliente_result.data[0] if cliente_result.data else {}

    # Usa IA para gerar treino
    treino_ia = generate_personalized_workout(cliente, num_dias, nivel_experiencia, tem_lesao, local_lesao)

    # Cria o treino no banco
    result_treino = (
        supabase.table("treinos")
        .insert({
            "cliente_id": cliente_id,
            "nivel_experiencia": nivel_experiencia,
            "tem_lesao": tem_lesao,
            "local_lesao": local_lesao,
            "num_dias": num_dias
        })
        .execute()
    )

    if not result_treino.data:
        return None

    treino_id = result_treino.data[0]["id"]

    # Adiciona exercícios do treino gerado pela IA
    ordem_geral = 1
    if "dias" in treino_ia:
        for dia_data in treino_ia["dias"]:
            dia = dia_data.get("dia", 1)
            if "exercicios" in dia_data:
                for exercicio_data in dia_data["exercicios"]:
                    # Verifica se o exercício existe na tabela, se não, cria
                    exercicio_nome = exercicio_data.get("nome", "Exercício")
                    exercicio_result = supabase.table("exercicios").select("id").ilike("nome", exercicio_nome).limit(1).execute()
                    
                    if exercicio_result.data:
                        exercicio_id = exercicio_result.data[0]["id"]
                    else:
                        # Cria exercício novo
                        novo_exercicio = supabase.table("exercicios").insert({
                            "nome": exercicio_nome,
                            "nivel_experiencia": nivel_experiencia,
                            "descricao": exercicio_data.get("observacoes", "")
                        }).execute()
                        exercicio_id = novo_exercicio.data[0]["id"] if novo_exercicio.data else None
                    
                    if exercicio_id:
                        supabase.table("treino_exercicios").insert({
                            "treino_id": treino_id,
                            "exercicio_id": exercicio_id,
                            "series": exercicio_data.get("series", 3),
                            "repeticoes": exercicio_data.get("repeticoes", "12-15"),
                            "ordem": ordem_geral,
                            "dia": dia
                        }).execute()
                        ordem_geral += 1

    # Retorna o treino completo com exercícios
    return buscar_treino_por_id(treino_id)

def buscar_treino_por_id(treino_id):
    """
    Busca um treino completo com seus exercícios
    """
    supabase = get_supabase()
    
    # Busca o treino
    result_treino = (
        supabase.table("treinos")
        .select("*")
        .eq("id", treino_id)
        .limit(1)
        .execute()
    )
    
    if not result_treino.data:
        return None
    
    treino = dict(result_treino.data[0])
    
    # Busca as relações treino-exercício
    result_relacoes = (
        supabase.table("treino_exercicios")
        .select("*")
        .eq("treino_id", treino_id)
        .order("ordem")
        .execute()
    )
    
    treino["exercicios"] = []
    
    if result_relacoes.data:
        # Busca os exercícios um por um
        for rel in result_relacoes.data:
            exercicio_result = (
                supabase.table("exercicios")
                .select("*")
                .eq("id", rel["exercicio_id"])
                .limit(1)
                .execute()
            )
            if exercicio_result.data:
                exercicio = dict(exercicio_result.data[0])
                exercicio.update(rel)
                treino["exercicios"].append(exercicio)
    
    return treino

def buscar_treinos_por_cliente(cliente_id):
    """
    Busca todos os treinos de um cliente
    """
    supabase = get_supabase()
    
    result = (
        supabase.table("treinos")
        .select("*")
        .eq("cliente_id", cliente_id)
        .order("data_criacao", desc=True)
        .execute()
    )
    
    treinos = []
    for treino in result.data or []:
        treino_completo = buscar_treino_por_id(treino["id"])
        if treino_completo:
            treinos.append(treino_completo)
    
    return treinos
