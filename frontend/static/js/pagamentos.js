console.log("pagamentos.js carregado!");

let clienteSelecionado = null;
let listaClientesInicial = [];

function formatarDataBr(dataStr) {
    if (!dataStr) return "";
    const [ano, mes, dia] = dataStr.split("-");
    return `${dia}/${mes}/${ano}`;
}

function formatarNomePlano(plano) {
    if (!plano) return "";
    return plano.charAt(0).toUpperCase() + plano.slice(1);
}

function renderizarTabelaPagamentos(lista) {
    const tbody = document.getElementById("bodyTabelaListaClientes");
    tbody.innerHTML = "";

    lista.forEach(cliente => {
        const tr = document.createElement("tr");
        tr.className = "clienteIndividual";
        tr.dataset.cliente = JSON.stringify(cliente);

        tr.innerHTML = `
            <td class="Nome" data-label="Cliente">${cliente.cliente_nome || ""}</td>
            <td data-label="Plano">${formatarNomePlano(cliente.plano)}</td>
            <td data-label="Vencimento">${formatarDataBr(cliente.data_vencimento)}</td>
            <td data-label="Último Pagamento">${formatarDataBr(cliente.ultimo_pagamento)}</td>
            <td class="Status" data-label="Status"><span class="${cliente.status || ''}">${cliente.status || ""}</span></td>
        `;

        tr.addEventListener("click", () => selecionarCliente(cliente));
        tbody.appendChild(tr);
    });
}

function selecionarCliente(cliente) {
    clienteSelecionado = cliente;
    
    // Preencher os dados na direita
    document.getElementById("cliente-nome-titulo").textContent = cliente.cliente_nome;
    document.getElementById("cliente-plano").textContent = formatarNomePlano(cliente.plano);
    document.getElementById("cliente-valor").textContent = cliente.valor || "R$ 0,00";
    document.getElementById("cliente-vencimento").textContent = formatarDataBr(cliente.data_vencimento);
    document.getElementById("cliente-ultimo-pagamento").textContent = formatarDataBr(cliente.ultimo_pagamento);
    const statusSpan = document.getElementById("cliente-status");
    statusSpan.textContent = cliente.status;
    statusSpan.className = cliente.status || "";

    // Mostrar ou não as opções de pagamento (se status for Pendente ou Inadimplente)
    const opcoesPagamento = document.getElementById("opcoes-pagamento");
    if (cliente.status === "Inadimplente") {
        opcoesPagamento.style.display = "block";
    } else if (cliente.status === "Pendente") {
        opcoesPagamento.style.display = "none";
    } else {
        opcoesPagamento.style.display = "none";
    }

    // Mostrar o cliente selecionado
    document.getElementById("cliente-selecionado").style.display = "block";
    document.getElementById("nenhum-cliente").style.display = "none";
}

function limparSelecao() {
    clienteSelecionado = null;
    document.getElementById("cliente-selecionado").style.display = "none";
    document.getElementById("nenhum-cliente").style.display = "block";
}

async function confirmarPagamento() {
    if (!clienteSelecionado) {
        alert("Nenhum cliente selecionado!");
        return;
    }

    if (!confirm(`Tem certeza que deseja confirmar o pagamento para ${clienteSelecionado.cliente_nome}?`)) {
        return;
    }

    // Pegar o tipo de pagamento (apenas se o cliente for inadimplente)
    let tipoPagamento = "atual";
    const opcoesPagamentoDiv = document.getElementById("opcoes-pagamento");
    if (opcoesPagamentoDiv.style.display === "block") {
        const selecionado = document.querySelector('input[name="tipo-pagamento-modal"]:checked');
        tipoPagamento = selecionado ? selecionado.value : "atual";
    }

    // Criar o formulário para enviar
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/registrar-pagamento/${clienteSelecionado.cliente_id}`;
    
    const inputTipoPagamento = document.createElement('input');
    inputTipoPagamento.type = 'hidden';
    inputTipoPagamento.name = 'tipo_pagamento';
    inputTipoPagamento.value = tipoPagamento;
    
    form.appendChild(inputTipoPagamento);
    document.body.appendChild(form);
    form.submit();
}

async function buscarPagamentos(termo) {
    try {
        const response = await fetch(`/pesquisar-pagamentos?termo=${encodeURIComponent(termo)}`);
        const pagamentos = await response.json();
        renderizarTabelaPagamentos(pagamentos);
    } catch (error) {
        console.error("Erro ao pesquisar pagamentos:", error);
    }
}

// Listener para a barra de pesquisa
let debounceTimer;
document.getElementById("pesquisaPagamentos").addEventListener("input", function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        buscarPagamentos(this.value);
    }, 300);
});

document.getElementById("btn-limpar-selecao").addEventListener("click", limparSelecao);
document.getElementById("btn-confirmar-pagamento").addEventListener("click", confirmarPagamento);

// Carregar os dados iniciais
document.addEventListener("DOMContentLoaded", function() {
    listaClientesInicial = JSON.parse(
        document.getElementById("pagamentos-data").textContent
    );
    renderizarTabelaPagamentos(listaClientesInicial);
});
