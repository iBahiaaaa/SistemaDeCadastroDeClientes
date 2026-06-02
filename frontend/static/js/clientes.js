console.log("JS carregado!");
const botaoCadastrar = document.getElementById("botaoCadastrar");
const modalCadastro = document.getElementById("modalCadastro");
const btnCancelar = document.getElementById("btnCancelar");

botaoCadastrar.addEventListener("click", function() {

    console.log("Botão clicado!");
    modalCadastro.classList.add("ativo");
    

});

btnCancelar.addEventListener("click", function() {

    modalCadastro.classList.remove("ativo");

});