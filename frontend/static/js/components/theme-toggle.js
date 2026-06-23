const toggleTema = document.getElementById("toggle");
const usuarioMenu = document.querySelector(".usuarioMenu");
const usuarioMenuBotao = document.querySelector(".usuarioMenu-botao");

function aplicarTema(tema) {
    document.documentElement.dataset.theme = tema;
    localStorage.setItem("tema", tema);

    if (toggleTema) {
        toggleTema.checked = tema === "dark";
    }
}

function carregarTemaInicial() {
    const temaSalvo = localStorage.getItem("tema");
    if (temaSalvo === "light" || temaSalvo === "dark") {
        aplicarTema(temaSalvo);
        return;
    }

    const prefereClaro = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
    aplicarTema(prefereClaro ? "light" : "dark");
}

carregarTemaInicial();

if (toggleTema) {
    toggleTema.addEventListener("change", function() {
        aplicarTema(toggleTema.checked ? "dark" : "light");
    });
}

if (usuarioMenu && usuarioMenuBotao) {
    usuarioMenuBotao.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        usuarioMenu.classList.toggle("aberto");
    });

    document.addEventListener("click", function() {
        usuarioMenu.classList.remove("aberto");
    });

    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape") {
            usuarioMenu.classList.remove("aberto");
        }
    });
}
