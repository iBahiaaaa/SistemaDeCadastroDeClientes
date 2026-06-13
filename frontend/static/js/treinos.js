console.log("Treinos JS carregado!");

let clienteSelecionado = null;
let debounceTimer = null;

const inputPesquisa = document.getElementById("pesquisaAluno");
const resultadosPesquisa = document.getElementById("resultadosPesquisa");
const cardAlunoSelecionado = document.getElementById("cardAlunoSelecionado");
const formGerarTreino = document.getElementById("formGerarTreino");
const listaTreinos = document.getElementById("listaTreinos");
const temLesaoSelect = document.getElementById("temLesao");
const campoLocalLesao = document.getElementById("campoLocalLesao");

// Evento de pesquisa de alunos
inputPesquisa.addEventListener("input", function() {
    clearTimeout(debounceTimer);
    const termo = this.value.trim();
    if (termo.length < 2) {
        resultadosPesquisa.innerHTML = "";
        return;
    }
    if (termo.length >= 2) {
        debounceTimer = setTimeout(() => pesquisarClientes(termo), 300);
    }
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
    formGerarTreino.style.display = "block";
    listaTreinos.style.display = "none";
});

document.getElementById("btnCancelarGerar").addEventListener("click", function() {
    formGerarTreino.style.display = "none";
});

document.getElementById("btnVerTreinos").addEventListener("click", function() {
    if (clienteSelecionado) {
        carregarTreinosCliente();
    }
});

document.getElementById("btnConfirmarGerar").addEventListener("click", function() {
    gerarTreino();
});

async function pesquisarClientes(termo) {
    try {
        const response = await fetch(`/pesquisar?termo=${encodeURIComponent(termo)}`);
        const clientes = await response.json();
        
        resultadosPesquisa.innerHTML = "";
        
        if (clientes.length === 0) {
            resultadosPesquisa.innerHTML = "<p>Nenhum aluno encontrado</p>";
            return;
        }
        
        clientes.forEach(cliente => {
            const div = document.createElement("div");
            div.className = "resultado-pesquisa-item";
            div.innerHTML = `
                <h4>${cliente.nome}</h4>
                <p>WhatsApp: ${cliente.whatsapp || "Não informado"}</p>
            `;
            div.addEventListener("click", () => selecionarCliente(cliente));
            resultadosPesquisa.appendChild(div);
        });
    } catch (erro) {
        console.error("Erro ao pesquisar clientes:", erro);
    }
}

function selecionarCliente(cliente) {
    clienteSelecionado = cliente;
    resultadosPesquisa.innerHTML = "";
    inputPesquisa.value = "";
    cardAlunoSelecionado.style.display = "block";
    document.getElementById("nomeAlunoSelecionado").textContent = cliente.nome;
    document.getElementById("infoAlunoSelecionado").textContent = `Plano: ${cliente.plano || "Não informado"} | Status: ${cliente.status}";
    listaTreinos.style.display = "none";
    formGerarTreino.style.display = "none";
}

async function carregarTreinosCliente() {
    try {
        const response = await fetch(`/treinos/cliente/${clienteSelecionado.id}`);
        const treinos = await response.json();
        
        listaTreinos.style.display = "block";
        formGerarTreino.style.display = "none";
        const cardsTreinos = document.getElementById("cardsTreinos");
        cardsTreinos.innerHTML = "";
        
        if (treinos.length === 0) {
            cardsTreinos.innerHTML = "<p>Nenhum treino encontrado para este aluno</p>";
            return;
        }
        
        treinos.forEach(treino => {
            const div = document.createElement("div");
            div.className = "cardTreino";
            
            let exerciciosHtml = treino.exercicios.map(ex => `
                <div class="exercicio-item">
                    <h4>${ex.nome}</h4>
                    <p>Grupo Muscular: ${ex.grupo_muscular}</p>
                    <p>Séries: ${ex.series} | Repetições: ${ex.repeticoes}</p>
                </div>
            `).join("");
            
            const dataCriacao = new Date(treino.data_criacao).toLocaleDateString("pt-BR");
            const nivelTexto = treino.nivel_experiencia.charAt(0).toUpperCase() + treino.nivel_experiencia.slice(1);
            let lesaoTexto = treino.tem_lesao ? ` | Lesão: ${treino.local_lesao}` : "";
            
            div.innerHTML = `
                <h3>Treino de ${dataCriacao}</h3>
                <span>Nível: ${nivelTexto}${lesaoTexto}</span>
                <div style="margin-top: 12px;">
                    ${exerciciosHtml}
                </div>
            `;
            cardsTreinos.appendChild(div);
        });
    } catch (erro) {
        console.error("Erro ao carregar treinos:", erro);
        alert("Erro ao carregar treinos do aluno");
    }
}

async function gerarTreino() {
    try {
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
