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
const inputEmail = document.getElementById("modalEmail");
const inputWhatsapp = document.getElementById("modalWhatsapp");
const inputEndereco = document.getElementById("modalEndereco");
const inputEmergencia = document.getElementById("modalEmergencia");
const inputIdade = document.getElementById("modalIdade");
const inputPeso = document.getElementById("modalPeso");
const inputAltura = document.getElementById("modalAltura");
const inputObjetivo = document.getElementById("modalObjetivo");
const inputPlano = document.getElementById("modalPlano");
const inputValorPlano = document.getElementById("modalValorPlano");
const inputStatus = document.getElementById("modalStatus");
const inputMatricula = document.getElementById("modalMatricula");
const inputVencimento = document.getElementById("modalVencimento");
const inputUltimoPagamento = document.getElementById("modalUltimoPagamento");
const inputObs = document.getElementById("modalObservacoes");
const linkWppEmergencia = document.getElementById("linkWppEmergencia");
const linkWppEmergenciaAnchor = linkWppEmergencia.querySelector("a");
const rowAtivacao = document.getElementById("rowAtivacao");
const inputAtivacaoCodigo = document.getElementById("modalAtivacaoCodigo");

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
    inputEmail.value = "";
    inputWhatsapp.value = "";
    inputEndereco.value = "";
    inputEmergencia.value = "";
    inputIdade.value = "";
    inputPeso.value = "";
    inputAltura.value = "";
    inputObjetivo.value = "";
    inputPlano.value = "mensal";
    inputValorPlano.value = "";
    inputStatus.value = "Pago"; // Status padrão
    inputMatricula.value = dataMatricula; // Preenche com data de hoje
    inputVencimento.value = dataVencimento; // Preenche com data daqui a 1 mês
    inputUltimoPagamento.value = ""; // Limpa o campo de último pagamento
    inputObs.value = "";
    inputAtivacaoCodigo.value = "";
    rowAtivacao.style.display = "none";

    // Esconder o link do WhatsApp de emergência para novo cadastro
    atualizarLinkWppEmergencia("");

    titulo.innerText = "Cadastrar Cliente";
    btnSalvar.innerText = "Salvar";
    btnExcluirModal.style.display = "none";
    btnConfirmarPagamento.style.display = "none";

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
        tr.dataset.email = cliente.email || "";
        tr.dataset.whatsapp = cliente.whatsapp || "";
        tr.dataset.endereco = cliente.endereco || "";
        tr.dataset.idade = cliente.idade || "";
        tr.dataset.peso = cliente.peso || "";
        tr.dataset.altura = cliente.altura || "";
        tr.dataset.objetivo = cliente.objetivo || "";
        tr.dataset.plano = cliente.plano || "";
        tr.dataset.valor = cliente.valor_plano || "";
        tr.dataset.matricula = cliente.data_matricula || "";
        tr.dataset.vencimento = cliente.data_vencimento || "";
        tr.dataset.ultimo_pagamento = cliente.ultimo_pagamento || "";
        tr.dataset.emergencia = cliente.contato_emergencia || "";
        tr.dataset.status = cliente.status || "";
        tr.dataset.observacoes = cliente.observacoes || "";
        tr.dataset.activation_code = cliente.activation_code || "";
        tr.dataset.conta_ativa = String(cliente.conta_ativa || 0);

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
            <td class="Nome" data-label="Nome">${cliente.nome || ""}</td>
            <td data-label="Whatsapp">${whatsappHtml}</td>
            <td data-label="Matricula">${formatarDataBr(cliente.data_matricula)}</td>
            <td data-label="Plano">${cliente.plano ? cliente.plano.charAt(0).toUpperCase() + cliente.plano.slice(1) : ""}</td>
            <td data-label="Vencimento">${formatarDataBr(cliente.data_vencimento)}</td>
            <td class="Status" data-label="Status"><span class="${cliente.status || ''}">${cliente.status || ""}</span></td>
            <td class="Observacoes" data-label="Observacoes">${cliente.observacoes || ""}</td>
        `;

        // Adiciona evento de clique para editar
        tr.addEventListener("click", function() {
            inputId.value = this.dataset.id;
            inputNome.value = this.dataset.nome;
            inputEmail.value = this.dataset.email;
            inputWhatsapp.value = this.dataset.whatsapp;
            inputEndereco.value = this.dataset.endereco;
            inputEmergencia.value = this.dataset.emergencia;
            inputIdade.value = this.dataset.idade;
            inputPeso.value = this.dataset.peso;
            inputAltura.value = this.dataset.altura;
            inputObjetivo.value = this.dataset.objetivo;
            inputPlano.value = this.dataset.plano;
            inputValorPlano.value = this.dataset.valor;
            inputStatus.value = this.dataset.status;
            inputMatricula.value = this.dataset.matricula;
            inputVencimento.value = this.dataset.vencimento;
            inputUltimoPagamento.value = this.dataset.ultimo_pagamento || "";
            inputObs.value = this.dataset.observacoes;
            inputAtivacaoCodigo.value = "";
            rowAtivacao.style.display = "none";
            
            // Armazena o status do cliente para verificar se é inadimplente
            statusClienteAtual = this.dataset.status;

            if (this.dataset.email && this.dataset.activation_code && this.dataset.conta_ativa !== "1") {
                inputAtivacaoCodigo.value = this.dataset.activation_code;
                rowAtivacao.style.display = "flex";
            }

            // Atualizar o link do WhatsApp de emergência
            atualizarLinkWppEmergencia(this.dataset.emergencia);

            titulo.innerText = "Editar Cliente";
            btnSalvar.innerText = "Atualizar";

            // Mostrar botão excluir e configurar ação
            btnExcluirModal.style.display = "block";
            btnConfirmarPagamento.style.display = "flex";
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

// Elementos do NOVO modal de pagamento completo
const modalPagamento = document.getElementById("modalPagamento");
const formModalPagamento = document.getElementById("formModalPagamento");
const btnCancelarPagamentoModal = document.getElementById("btnCancelarPagamentoModal");
const secaoInadimplente = document.getElementById("secaoInadimplente");

// Campos do modal de pagamento
const pagamentoValor = document.getElementById("pagamentoValor");
const pagamentoPlano = document.getElementById("pagamentoPlano");
const pagamentoData = document.getElementById("pagamentoData");
const pagamentoVencimento = document.getElementById("pagamentoVencimento");
const pagamentoObs = document.getElementById("pagamentoObs");

// Variável para armazenar o status do cliente atual
let statusClienteAtual = "";
// Variável para armazenar o cliente atual (para dados padrão)
let clienteAtual = null;

// Função para formatar valor monetário (para o campo pagamentoValor)
function formatarValorMonetario(input) {
    input.addEventListener("input", function(e) {
        let value = e.target.value.replace(/\D/g, "");
        if (value === "") {
            e.target.value = "";
            return;
        }
        
        value = (value / 100).toFixed(2) + "";
        value = value.replace(".", ",");
        value = value.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
        e.target.value = "R$ " + value;
    });
}

// Aplica a máscara no campo de valor do pagamento
formatarValorMonetario(pagamentoValor);

// Função para abrir o modal de pagamento completo
function abrirModalPagamento() {
    if (!inputId.value) {
        alert("Você precisa editar um cliente para confirmar o pagamento!");
        return;
    }
    
    // Preenche os campos do modal com os dados do cliente atual
    pagamentoValor.value = inputValorPlano.value; // Usa o valor do plano do cliente
    pagamentoPlano.value = inputPlano.value; // Usa o plano do cliente
    pagamentoData.value = formatarDataParaInput(new Date()); // Data de hoje
    pagamentoVencimento.value = inputVencimento.value; // Data de vencimento atual
    pagamentoObs.value = ""; // Limpa as observações
    
    // Mostra/oculta a seção de inadimplentes
    if (statusClienteAtual === "Inadimplente") {
        secaoInadimplente.style.display = "block";
    } else {
        secaoInadimplente.style.display = "none";
    }
    
    // Abre o modal de pagamento
    modalPagamento.classList.add("ativo");
    overlayModal.classList.add("ativo");
}

// Função para fechar o modal de pagamento completo
function fecharModalPagamento() {
    modalPagamento.classList.remove("ativo");
    overlayModal.classList.remove("ativo");
}

// Botão para abrir o modal de pagamento (o botão "Confirmar Pagamento" no modal de edição)
btnConfirmarPagamento.addEventListener("click", abrirModalPagamento);

// Botão para cancelar o pagamento modal
btnCancelarPagamentoModal.addEventListener("click", fecharModalPagamento);

// Submissão do form do modal de pagamento
formModalPagamento.addEventListener("submit", function(e) {
    e.preventDefault(); // Previne o comportamento padrão de submissão
    
    // Configura o action do form para a rota correta
    formModalPagamento.action = `/registrar-pagamento/${inputId.value}`;
    
    // Submete o form!
    formModalPagamento.submit();
});

// Fecha o modal de pagamento ao clicar no overlay (apenas se o modal de clientes não estiver aberto? Ou sempre?)
overlayModal.addEventListener("click", function() {
    if (modalPagamento.classList.contains("ativo")) {
        fecharModalPagamento();
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
