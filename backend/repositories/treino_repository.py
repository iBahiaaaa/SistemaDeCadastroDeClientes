from backend.database.connection import get_supabase

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

def criar_treino(cliente_id, nivel_experiencia, tem_lesao, local_lesao=None):
    """
    Cria um novo treino para o cliente, com exercícios adequados
    """
    supabase = get_supabase()
    
    # Primeiro, busca os exercícios adequados
    exercicios_adequadados = buscar_exercicios(nivel_experiencia, local_lesao)
    
    # Cria o treino
    result_treino = (
        supabase.table("treinos")
        .insert({
            "cliente_id": cliente_id,
            "nivel_experiencia": nivel_experiencia,
            "tem_lesao": tem_lesao,
            "local_lesao": local_lesao
        })
        .execute()
    )
    
    if not result_treino.data:
        return None
    
    treino_id = result_treino.data[0]["id"]
    
    # Define séries e repetições com base no nível
    if nivel_experiencia == "iniciante":
        series_padrao = 3
        repeticoes_padrao = "12-15"
    elif nivel_experiencia == "intermediario":
        series_padrao = 4
        repeticoes_padrao = "10-12"
    else:  # avançado
        series_padrao = 4
        repeticoes_padrao = "8-10"
    
    # Associa os exercícios ao treino
    for idx, exercicio in enumerate(exercicios_adequadados, start=1):
        supabase.table("treino_exercicios").insert({
            "treino_id": treino_id,
            "exercicio_id": exercicio["id"],
            "series": series_padrao,
            "repeticoes": repeticoes_padrao,
            "ordem": idx
        }).execute()
    
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
