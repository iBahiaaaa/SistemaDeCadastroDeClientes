console.log("funcionarios.js carregado!");

const pesquisaFuncionarios = document.getElementById("pesquisaFuncionarios");
const listaUsuarios = document.getElementById("listaUsuarios");

function renderizarUsuarios(usuarios) {
    listaUsuarios.innerHTML = "";

    usuarios.forEach(usuario => {
        const card = document.createElement("div");
        card.className = "cardUsuario";

        card.innerHTML = `
            <div class="cardUsuario-topo">
                <div>
                    <strong>${usuario.nome_exibicao || "Usuário"}</strong>
                    <small>${usuario.email || ""}</small>
                </div>
                ${usuario.possui_vinculo_cliente ? '<span class="tagVinculo">Vinculado a cliente</span>' : ''}
            </div>
            <div class="cardUsuario-conteudo">
                <label for="cargo-${usuario.id}">Cargo</label>
                <form action="/funcionarios/${usuario.id}/cargo" method="POST" style="display: flex; gap: 8px; align-items: center;">
                    <select name="cargo" id="cargo-${usuario.id}">
                        <option value="ADM" ${usuario.cargo === "ADM" ? "selected" : ""}>ADM</option>
                        <option value="FUNCIONARIO" ${usuario.cargo === "FUNCIONARIO" ? "selected" : ""}>FUNCIONÁRIO</option>
                        <option value="INSTRUTOR" ${usuario.cargo === "INSTRUTOR" ? "selected" : ""}>INSTRUTOR</option>
                        <option value="FINANCEIRO" ${usuario.cargo === "FINANCEIRO" ? "selected" : ""}>FINANCEIRO</option>
                        <option value="ALUNO" ${usuario.cargo === "ALUNO" ? "selected" : ""}>ALUNO</option>
                    </select>
                    <button type="submit" class="botaoSalvarCargo">Salvar</button>
                </form>
            </div>
        `;

        listaUsuarios.appendChild(card);
    });
}

function buscarUsuarios(termo) {
    fetch(`/pesquisar-funcionarios?termo=${encodeURIComponent(termo)}`)
        .then(response => response.json())
        .then(usuarios => renderizarUsuarios(usuarios))
        .catch(error => console.error("Erro ao pesquisar funcionários:", error));
}

let debounceTimer;
pesquisaFuncionarios.addEventListener("input", function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        buscarUsuarios(this.value);
    }, 300);
});

document.addEventListener("DOMContentLoaded", function() {
    let usuariosIniciais = JSON.parse(
        document.getElementById("funcionarios-data").textContent
    );

    renderizarUsuarios(usuariosIniciais);
});
