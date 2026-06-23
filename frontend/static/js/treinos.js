console.log("treinos.js carregado!");

let clienteSelecionado = null;
let listaClientesInicial = [];

const inputPesquisa = document.getElementById("pesquisaAluno");
const temLesaoSelect = document.getElementById("temLesao");
const campoLocalLesao = document.getElementById("campoLocalLesao");

function formatarNomePlano(plano) {
    if (!plano) return "";
    return plano.charAt(0).toUpperCase() + plano.slice(1);
}

function renderizarTabelaTreinos(lista) {
    const tbody = document.getElementById("bodyTabelaListaClientes");
    tbody.innerHTML = "";

    lista.forEach(cliente => {
        const tr = document.createElement("tr");
        tr.className = "clienteIndividual";
        tr.dataset.cliente = JSON.stringify(cliente);

        tr.innerHTML = `
            <td class="Nome" data-label="Aluno">${cliente.nome || ""}</td>
            <td data-label="Plano">${formatarNomePlano(cliente.plano)}</td>
            <td class="Status" data-label="Status"><span class="status ${cliente.status || ""}">${cliente.status || ""}</span></td>
        `;

        tr.addEventListener("click", () => selecionarCliente(cliente));
        tbody.appendChild(tr);
    });
}

function selecionarCliente(cliente) {
    clienteSelecionado = cliente;

    // Preencher os dados na direita
    document.getElementById("nomeAlunoSelecionado").textContent = cliente.nome;
    document.getElementById("alunoPlano").textContent = formatarNomePlano(cliente.plano);
    const statusSpan = document.getElementById("alunoStatus");
    statusSpan.textContent = cliente.status;
    statusSpan.className = `status ${cliente.status || ""}`;

    // Mostrar o aluno selecionado, esconder o "nenhum aluno"
    document.getElementById("alunoSelecionado").style.display = "block";
    document.getElementById("nenhumAluno").style.display = "none";

    // Esconder o form e lista de treinos inicialmente
    document.getElementById("formGerarTreino").style.display = "none";
    document.getElementById("listaTreinos").style.display = "none";
}

async function carregarTreinosCliente() {
    try {
        const response = await fetch(`/treinos/cliente/${clienteSelecionado.id}`);
        const treinos = await response.json();

        document.getElementById("listaTreinos").style.display = "block";
        document.getElementById("formGerarTreino").style.display = "none";
        const cardsTreinos = document.getElementById("cardsTreinos");
        cardsTreinos.innerHTML = "";

        if (treinos.length === 0) {
            cardsTreinos.innerHTML = "<p style='color: var(--textoSuave);'>Nenhum treino encontrado para este aluno</p>";
            return;
        }

        treinos.forEach(treino => {
            const div = document.createElement("div");
            div.className = "cardTreino";

            // Agrupa exercícios por dia
            const exerciciosPorDia = {};
            treino.exercicios.forEach(exercicio => {
                const dia = exercicio.dia || 1;
                if (!exerciciosPorDia[dia]) {
                    exerciciosPorDia[dia] = [];
                }
                exerciciosPorDia[dia].push(exercicio);
            });

            let diasHtml = "";
            Object.keys(exerciciosPorDia).sort((a, b) => a - b).forEach(dia => {
                const exerciciosDia = exerciciosPorDia[dia];
                diasHtml += `
                    <div class="treino-dia">
                        <h4>Dia ${dia}</h4>
                        ${exerciciosDia.map(ex => `
                            <div class="exercicio-item">
                                <h5>${ex.nome}</h5>
                                <p>Grupo Muscular: ${ex.grupo_muscular}</p>
                                <p>Séries: ${ex.series} | Repetições: ${ex.repeticoes}</p>
                                <div class="exercicio-acoes">
                                    <button class="btnRemoverExercicio" data-treino-id="${treino.id}" data-exercicio-id="${ex.id}">
                                        <i class="fa-solid fa-trash"></i> Remover
                                    </button>
                                </div>
                            </div>
                        `).join("")}
                    </div>
                `;
            });

            const dataCriacao = new Date(treino.data_criacao).toLocaleDateString("pt-BR");
            const nivelTexto = treino.nivel_experiencia.charAt(0).toUpperCase() + treino.nivel_experiencia.slice(1);
            let lesaoTexto = treino.tem_lesao ? ` | Lesão: ${treino.local_lesao}` : "";

            div.innerHTML = `
                <h3>Treino de ${dataCriacao}</h3>
                <span>Nível: ${nivelTexto}${lesaoTexto}</span>
                <div style="margin-top: 12px;">
                    ${diasHtml}
                </div>
                <div style="margin-top: 12px;">
                    <button class="btnAdicionarExercicio" data-treino-id="${treino.id}">
                        <i class="fa-solid fa-plus"></i> Adicionar Exercício
                    </button>
                </div>
            `;
            cardsTreinos.appendChild(div);
        });

        // Adiciona listeners para os botões
        document.querySelectorAll(".btnRemoverExercicio").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const treinoId = e.target.closest("button").dataset.treinoId;
                const exercicioId = e.target.closest("button").dataset.exercicioId;
                removerExercicio(treinoId, exercicioId);
            });
        });

        document.querySelectorAll(".btnAdicionarExercicio").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const treinoId = e.target.closest("button").dataset.treinoId;
                abrirModalAdicionarExercicio(treinoId);
            });
        });
    } catch (erro) {
        console.error("Erro ao carregar treinos:", erro);
        alert("Erro ao carregar treinos do aluno");
    }
}

async function gerarTreino() {
    try {
        const numDias = document.getElementById("numDias").value;
        const nivel = document.getElementById("nivelExperiencia").value;
        const temLesao = document.getElementById("temLesao").value;
        const localLesao = document.getElementById("localLesao").value;

        if (temLesao === "true" && !localLesao) {
            alert("Selecione o local da lesão");
            return;
        }

        const response = await fetch("/treinos/gerar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                cliente_id: clienteSelecionado.id,
                numDias: numDias,
                nivel_experiencia: nivel,
                tem_lesao: temLesao,
                local_lesao: temLesao === "true" ? localLesao : null
            })
        });

        if (!response.ok) {
            const erro = await response.json();
            alert(erro.erro || "Erro ao gerar treino");
            return;
        }

        alert("Treino gerado com sucesso!");
        carregarTreinosCliente();
    } catch (erro) {
        console.error("Erro ao gerar treino:", erro);
        alert("Erro ao gerar treino");
    }
}

let treinoAtualId = null;
let exerciciosDisponiveis = [];

async function removerExercicio(treinoId, exercicioId) {
    if (!confirm("Tem certeza que quer remover este exercício?")) return;
    try {
        const response = await fetch(`/treinos/${treinoId}/exercicios/${exercicioId}`, {
            method: "DELETE"
        });
        if (!response.ok) {
            const erro = await response.json();
            alert(erro.erro || "Erro ao remover exercício");
            return;
        }
        alert("Exercício removido com sucesso!");
        carregarTreinosCliente();
    } catch (erro) {
        console.error("Erro ao remover exercício:", erro);
        alert("Erro ao remover exercício");
    }
}

async function abrirModalAdicionarExercicio(treinoId) {
    treinoAtualId = treinoId;
    try {
        // Busca treino para pegar num_dias
        const treinoResponse = await fetch(`/treinos/cliente/${clienteSelecionado.id}`);
        const treinos = await treinoResponse.json();
        const treino = treinos.find(t => t.id == treinoId);
        
        if (!treino) return;
        
        // Preenche os dias
        const selectDia = document.getElementById("selectDia");
        selectDia.innerHTML = "";
        for (let i = 1; i <= (treino.num_dias || 3); i++) {
            const option = document.createElement("option");
            option.value = i;
            option.textContent = `Dia ${i}`;
            selectDia.appendChild(option);
        }
        
        // Busca exercícios disponíveis
        const exerciciosResponse = await fetch(`/exercicios`);
        exerciciosDisponiveis = await exerciciosResponse.json();
        const selectExercicio = document.getElementById("selectExercicio");
        selectExercicio.innerHTML = "";
        exerciciosDisponiveis.forEach(ex => {
            const option = document.createElement("option");
            option.value = ex.id;
            option.textContent = `${ex.nome} (${ex.grupo_muscular})`;
            selectExercicio.appendChild(option);
        });
        
        // Mostra o modal
        const modal = document.getElementById("modalAdicionarExercicio");
        modal.style.display = "flex";
    } catch (erro) {
        console.error("Erro ao abrir modal:", erro);
        alert("Erro ao abrir modal");
    }
}

async function adicionarExercicio() {
    const dia = document.getElementById("selectDia").value;
    const exercicioId = document.getElementById("selectExercicio").value;
    const series = document.getElementById("inputSeries").value;
    const repeticoes = document.getElementById("inputRepeticoes").value;
    
    if (!exercicioId) {
        alert("Selecione um exercício");
        return;
    }
    
    try {
        const response = await fetch(`/treinos/${treinoAtualId}/exercicios`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                exercicio_id: exercicioId,
                dia: dia,
                series: series,
                repeticoes: repeticoes
            })
        });
        
        if (!response.ok) {
            const erro = await response.json();
            alert(erro.erro || "Erro ao adicionar exercício");
            return;
        }
        
        alert("Exercício adicionado com sucesso!");
        fecharModalAdicionarExercicio();
        carregarTreinosCliente();
    } catch (erro) {
        console.error("Erro ao adicionar exercício:", erro);
        alert("Erro ao adicionar exercício");
    }
}

function fecharModalAdicionarExercicio() {
    const modal = document.getElementById("modalAdicionarExercicio");
    modal.style.display = "none";
}

// Event listeners para o modal
document.addEventListener("click", (e) => {
    const btnCancelar = document.getElementById("btnCancelarAdicionarExercicio");
    const btnConfirmar = document.getElementById("btnConfirmarAdicionarExercicio");
    
    if (e.target === btnCancelar) {
        fecharModalAdicionarExercicio();
    }
    
    if (e.target === btnConfirmar) {
        adicionarExercicio();
    }
});

async function pesquisarTreinos(termo) {
    try {
        const response = await fetch(`/pesquisar-treinos?termo=${encodeURIComponent(termo)}`);
        const clientes = await response.json();
        renderizarTabelaTreinos(clientes);
    } catch (erro) {
        console.error("Erro ao pesquisar:", erro);
    }
}

// Evento de pesquisa
let debounceTimer;
inputPesquisa.addEventListener("input", function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        pesquisarTreinos(this.value);
    }, 300);
});

// Evento para mostrar campo de lesão
temLesaoSelect.addEventListener("change", function() {
    if (this.value === "true") {
        campoLocalLesao.style.display = "block";
    } else {
        campoLocalLesao.style.display = "none";
        document.getElementById("localLesao").value = "";
    }
});

// Eventos dos botões
document.getElementById("btnAbrirModalGerar").addEventListener("click", function() {
    document.getElementById("formGerarTreino").style.display = "block";
    document.getElementById("listaTreinos").style.display = "none";
});

document.getElementById("btnCancelarGerar").addEventListener("click", function() {
    document.getElementById("formGerarTreino").style.display = "none";
});

document.getElementById("btnVerTreinos").addEventListener("click", function() {
    if (clienteSelecionado) {
        carregarTreinosCliente();
    }
});

document.getElementById("btnConfirmarGerar").addEventListener("click", function() {
    gerarTreino();
});

// Carregar os dados iniciais
document.addEventListener("DOMContentLoaded", function() {
    listaClientesInicial = JSON.parse(
        document.getElementById("treinos-data").textContent
    );
    renderizarTabelaTreinos(listaClientesInicial);
});
