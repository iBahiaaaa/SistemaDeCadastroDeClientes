console.log("JS carregado!");
const botaoCadastrar = document.getElementById("botaoCadastrar");
const modalCadastro = document.getElementById("modalCadastro");
const overlayModal = document.getElementById("overlayModal");
const btnCancelar = document.getElementById("btnCancelar");

const titulo = document.getElementById("modalTitulo");
const btnSalvar = document.getElementById("btnSalvar");

const inputId = document.getElementById("id_cliente");
const inputNome = document.getElementById("modalNome");
const inputWhatsapp = document.getElementById("modalWhatsapp");
const inputEndereco = document.getElementById("modalEndereco");
const inputEmergencia = document.getElementById("modalEmergencia");
const inputPlano = document.getElementById("modalPlano");
const inputValorPlano = document.getElementById("modalValorPlano");
const inputStatus = document.getElementById("modalStatus");
const inputMatricula = document.getElementById("modalMatricula");
const inputVencimento = document.getElementById("modalVencimento");
const inputObs = document.getElementById("modalObservacoes");

const btnExcluirModal = document.getElementById("btnExcluirModal");
const formExcluirOculto = document.getElementById("formExcluirOculto");

botaoCadastrar.addEventListener("click", function() {

    console.log("Botão clicado!");

    inputId.value = "";
    inputNome.value = "";
    inputWhatsapp.value = "";
    inputEndereco.value = "";
    inputEmergencia.value = "";
    inputPlano.value = "";
    inputValorPlano.value = "";
    inputStatus.value = "Pago";
    inputMatricula.value = "";
    inputVencimento.value = "";
    inputObs.value = "";

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

document.querySelectorAll(".clienteIndividual").forEach(row => {
    row.addEventListener("click", function() {

        inputId.value = row.dataset.id;
        inputNome.value = row.dataset.nome;
        inputWhatsapp.value = row.dataset.whatsapp;
        inputEndereco.value = row.dataset.endereco;
        inputEmergencia.value = row.dataset.emergencia;
        inputPlano.value = row.dataset.plano;
        inputValorPlano.value = row.dataset.valor;
        inputStatus.value = row.dataset.status;
        inputMatricula.value = row.dataset.matricula;
        inputVencimento.value = row.dataset.vencimento;
        inputObs.value = row.dataset.observacoes;

        titulo.innerText = "Editar Cliente";
        btnSalvar.innerText = "Atualizar";
        
        // Mostrar botão excluir e configurar ação
        btnExcluirModal.style.display = "block";
        btnExcluirModal.onclick = function() {
            if (confirm('Tem certeza que deseja excluir este cliente?')) {
                formExcluirOculto.action = `/excluir/${row.dataset.id}`;
                formExcluirOculto.submit();
            }
        };

        abrirModal();
    });
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