console.log("JS carregado!");
const botaoCadastrar = document.getElementById("botaoCadastrar");
const modalCadastro = document.getElementById("modalCadastro");
const overlayModal = document.getElementById("overlayModal");
const btnCancelar = document.getElementById("btnCancelar");
const pesquisaClientes = document.getElementById("pesquisaClientes");
const tbodyClientes = document.getElementById("bodyTabelaListaClientes");

const titulo = document.getElementById("modalTitulo");
const btnSalvar = document.getElementById("btnSalvar");

const inputId = document.getElementById("id_cliente");
const inputNome = document.getElementById("modalNome");
const inputWhatsapp = document.getElementById("modalWhatsapp");
const inputEndereco = document.getElementById("modalEndereco");
const inputEmergencia = document.getElementById("modalEmergencia");
const inputPlano = document.getElementById("modalPlano");
const inputValorPlano = document.getElementById("modalValorPlano");
const inputPeriodoPlano = document.getElementById("modalPeriodoPlano");
const inputStatus = document.getElementById("modalStatus");
const inputMatricula = document.getElementById("modalMatricula");
const inputVencimento = document.getElementById("modalVencimento");
const inputUltimoPagamento = document.getElementById("modalUltimoPagamento");
const inputObs = document.getElementById("modalObservacoes");
const linkWppEmergencia = document.getElementById("linkWppEmergencia");
const linkWppEmergenciaAnchor = linkWppEmergencia.querySelector("a");

const btnExcluirModal = document.getElementById("btnExcluirModal");
const btnConfirmarPagamento = document.getElementById("btnConfirmarPagamento");
const formExcluirOculto = document.getElementById("formExcluirOculto");
const formPagamentoOculto = document.getElementById("formPagamentoOculto");

function limparNumeroParaWpp(numero) {
    return numero.replace(/\D/g, ""); // Remove tudo que não é dígito
}

function atualizarLinkWppEmergencia(numero) {
    if (numero) {
        const numeroLimpo = limparNumeroParaWpp(numero);
        linkWppEmergenciaAnchor.href = `https://wa.me/55${numeroLimpo}`;
        linkWppEmergencia.style.display = "inline-block";
    } else {
        linkWppEmergencia.style.display = "none";
    }
}

function formatarDataParaInput(data) {
    const ano = data.getFullYear();
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const dia = String(data.getDate()).padStart(2, '0');
    return `${ano}-${mes}-${dia}`;
}

function adicionarUmMes(data) {
    const novaData = new Date(data);
    novaData.setMonth(novaData.getMonth() + 1);
    return novaData;
}

botaoCadastrar.addEventListener("click", function() {

    console.log("Botão clicado!");

    const dataHoje = new Date();
    const dataMatricula = formatarDataParaInput(dataHoje);
    const dataVencimento = formatarDataParaInput(adicionarUmMes(dataHoje));

    inputId.value = "";
    inputNome.value = "";
    inputWhatsapp.value = "";
    inputEndereco.value = "";
    inputEmergencia.value = "";
    inputPlano.value = "";
    inputValorPlano.value = "";
    inputPeriodoPlano.value = "mensal";
    inputStatus.value = "Pago"; // Status padrão
    inputMatricula.value = dataMatricula; // Preenche com data de hoje
    inputVencimento.value = dataVencimento; // Preenche com data daqui a 1 mês
    inputUltimoPagamento.value = ""; // Limpa o campo de último pagamento
    inputObs.value = "";

    // Esconder o link do WhatsApp de emergência para novo cadastro
    atualizarLinkWppEmergencia("");

    titulo.innerText = "Cadastrar Cliente";
    btnSalvar.innerText = "Salvar";
    btnExcluirModal.style.display = "none";

    abrirModal();
});

btnCancelar.addEventListener("click", function() {
    modalCadastro.classList.remove("ativo");
    overlayModal.classList.remove("ativo");
});

overlayModal.addEventListener("click", function() {
    modalCadastro.classList.remove("ativo");
    overlayModal.classList.remove("ativo");
});

// Editar

function abrirModal() {
    modalCadastro.classList.add("ativo");
    overlayModal.classList.add("ativo");
}

function fecharModal() {
    modalCadastro.classList.remove("ativo");
    overlayModal.classList.remove("ativo");
}

btnCancelar.addEventListener("click", fecharModal);
overlayModal.addEventListener("click", fecharModal);

// Função para formatar datas no formato dd/mm/yyyy
function formatarDataBr(dataStr) {
    if (!dataStr) return "";
    const [ano, mes, dia] = dataStr.split("-");
    return `${dia}/${mes}/${ano}`;
}

// Função para renderizar a tabela de clientes
function renderizarTabelaClientes(clientes) {
    tbodyClientes.innerHTML = "";

    clientes.forEach(cliente => {
        const tr = document.createElement("tr");
        tr.className = "clienteIndividual";
        tr.dataset.id = cliente.id;
        tr.dataset.nome = cliente.nome || "";
        tr.dataset.whatsapp = cliente.whatsapp || "";
        tr.dataset.endereco = cliente.endereco || "";
        tr.dataset.plano = cliente.plano || "";
        tr.dataset.valor = cliente.valor_plano || "";
        tr.dataset.periodo_plano = cliente.periodo_plano || "mensal";
        tr.dataset.matricula = cliente.data_matricula || "";
        tr.dataset.vencimento = cliente.data_vencimento || "";
        tr.dataset.ultimo_pagamento = cliente.ultimo_pagamento || "";
        tr.dataset.emergencia = cliente.contato_emergencia || "";
        tr.dataset.status = cliente.status || "";
        tr.dataset.observacoes = cliente.observacoes || "";

        // Celula WhatsApp com link
        let whatsappHtml = cliente.whatsapp || "";
        if (cliente.whatsapp) {
            const numeroLimpo = limparNumeroParaWpp(cliente.whatsapp);
            whatsappHtml = `
                <div class="whatsapp-cell">
                    <span>${cliente.whatsapp}</span>
                    <a href="https://wa.me/55${numeroLimpo}" target="_blank" class="whatsapp-link" onclick="event.stopPropagation();">
                        <i class="fa-brands fa-whatsapp"></i>
                    </a>
                </div>
            `;
        }

        tr.innerHTML = `
            <td data-label="Nome">${cliente.nome || ""}</td>
            <td data-label="Whatsapp">${whatsappHtml}</td>
            <td data-label="Matricula">${formatarDataBr(cliente.data_matricula)}</td>
            <td data-label="Plano">${cliente.plano || ""}</td>
            <td data-label="Vencimento">${formatarDataBr(cliente.data_vencimento)}</td>
            <td data-label="Status" class="${cliente.status || ''}">${cliente.status || ""}</td>
            <td data-label="Observações">${cliente.observacoes || ""}</td>
        `;

        // Adiciona evento de clique para editar
        tr.addEventListener("click", function() {
            inputId.value = this.dataset.id;
            inputNome.value = this.dataset.nome;
            inputWhatsapp.value = this.dataset.whatsapp;
            inputEndereco.value = this.dataset.endereco;
            inputEmergencia.value = this.dataset.emergencia;
            inputPlano.value = this.dataset.plano;
            inputValorPlano.value = this.dataset.valor;
            inputPeriodoPlano.value = this.dataset.periodo_plano;
            inputStatus.value = this.dataset.status;
            inputMatricula.value = this.dataset.matricula;
            inputVencimento.value = this.dataset.vencimento;
            inputUltimoPagamento.value = this.dataset.ultimo_pagamento || "";
            inputObs.value = this.dataset.observacoes;

            // Atualizar o link do WhatsApp de emergência
            atualizarLinkWppEmergencia(this.dataset.emergencia);

            titulo.innerText = "Editar Cliente";
            btnSalvar.innerText = "Atualizar";

            // Mostrar botão excluir e configurar ação
            btnExcluirModal.style.display = "block";
            btnExcluirModal.onclick = function() {
                if (confirm('Tem certeza que deseja excluir este cliente?')) {
                    formExcluirOculto.action = `/excluir/${tr.dataset.id}`;
                    formExcluirOculto.submit();
                }
            };

            abrirModal();
        });

        tbodyClientes.appendChild(tr);
    });
}

// Função para registrar pagamento usando o botão do modal
btnConfirmarPagamento.addEventListener("click", function() {
    if (!inputId.value) {
        alert("Você precisa editar um cliente para confirmar o pagamento!");
        return;
    }
    
    if (confirm('Tem certeza que deseja registrar o pagamento deste cliente?')) {
        formPagamentoOculto.action = `/registrar-pagamento/${inputId.value}`;
        formPagamentoOculto.submit();
    }
});

// Função para fazer a pesquisa
async function buscarClientes(termo) {
    try {
        const response = await fetch(`/pesquisar?termo=${encodeURIComponent(termo)}`);
        const clientes = await response.json();
        renderizarTabelaClientes(clientes);
    } catch (error) {
        console.error("Erro ao pesquisar clientes:", error);
    }
}

// Listener para a barra de pesquisa
let debounceTimer;
pesquisaClientes.addEventListener("input", function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        buscarClientes(this.value);
    }, 300); // Debounce para não fazer requisições a cada tecla
});

// Fim do editar

// Máscaras de entrada
function aplicarMascaraTelefone(input) {
    input.addEventListener("input", function(e) {
        let value = e.target.value.replace(/\D/g, "");
        if (value.length > 11) value = value.slice(0, 11);
        
        if (value.length > 10) {
            // (99) 99999-9999
            e.target.value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, "($1) $2-$3");
        } else if (value.length > 6) {
            // (99) 9999-9999
            e.target.value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, "($1) $2-$3");
        } else if (value.length > 2) {
            // (99) 9999
            e.target.value = value.replace(/^(\d{2})(\d{0,5}).*/, "($1) $2");
        } else if (value.length > 0) {
            // (99
            e.target.value = value.replace(/^(\d{0,2}).*/, "($1");
        }
    });
}

function aplicarMascaraMoeda(input) {
    input.addEventListener("input", function(e) {
        let value = e.target.value.replace(/\D/g, "");
        
        // Converte para centavos
        value = (value / 100).toFixed(2) + "";
        value = value.replace(".", ",");
        
        // Adiciona separador de milhar
        value = value.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
        
        if (value === "NaN" || value === "0,00") {
            e.target.value = "";
        } else {
            e.target.value = "R$ " + value;
        }
    });
}

aplicarMascaraTelefone(inputWhatsapp);
aplicarMascaraTelefone(inputEmergencia);
aplicarMascaraMoeda(inputValorPlano);

// Atualizar o link do WhatsApp de emergência em tempo real
inputEmergencia.addEventListener("input", function() {
    atualizarLinkWppEmergencia(this.value);
});

// Atualizar data de vencimento quando a data de matrícula for alterada
inputMatricula.addEventListener("change", function() {
    if (this.value) {
        const dataMatricula = new Date(this.value);
        const dataVencimento = adicionarUmMes(dataMatricula);
        inputVencimento.value = formatarDataParaInput(dataVencimento);
    }
});
