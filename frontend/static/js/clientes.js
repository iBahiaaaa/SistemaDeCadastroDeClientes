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
const inputObs = document.getElementById("modalObservacoes");

botaoCadastrar.addEventListener("click", function() {

    console.log("Botão clicado!");

    modalCadastro.classList.add("ativo");
    overlayModal.classList.add("ativo");
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

botaoCadastrar.addEventListener("click", function() {

    inputId.value = "";
    inputNome.value = "";
    inputWhatsapp.value = "";
    inputEndereco.value = "";
    inputObs.value = "";

    titulo.innerText = "Cadastrar Cliente";
    btnSalvar.innerText = "Salvar";

    abrirModal();
});

btnCancelar.addEventListener("click", fecharModal);
overlayModal.addEventListener("click", fecharModal);

document.querySelectorAll(".btnEditar").forEach(btn => {
    btn.addEventListener("click", function() {

        inputId.value = btn.dataset.id;
        inputNome.value = btn.dataset.nome;
        inputWhatsapp.value = btn.dataset.whatsapp;
        inputEndereco.value = btn.dataset.endereco;
        inputObs.value = btn.dataset.observacoes;

        titulo.innerText = "Editar Cliente";
        btnSalvar.innerText = "Atualizar";

        abrirModal();
    });
});

// Fim do editar