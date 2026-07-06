// ======================================
// INICIALIZACIÓN
// ======================================

document.addEventListener("DOMContentLoaded", () => {

    init();

});

// ======================================
// VARIABLES GLOBALES
// ======================================

let searchTimeout;

// ======================================
// FUNCIONES PRINCIPALES
// ======================================

function init() {

    document.addEventListener("input", manejarInput);

    document.addEventListener("change", manejarChange);

    document.addEventListener("click", manejarClick);

}

function manejarInput(event) {
    if (event.target.id !== "searchInput") return;

    const clearButton = document.getElementById("clearSearch");

    if (clearButton) {

        clearButton.style.display =
            event.target.value.trim() ? "flex" : "none";

    }

    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {

        const searchInput = event.target;
        const perPageSelect = document.getElementById("per_page");

        const params = new URLSearchParams();

        params.append("q", searchInput.value);
        params.append("per_page", perPageSelect.value);

        cargarUsuarios(`/admin?${params.toString()}`);

    }, 300);

}

function manejarChange(event) {
    if (event.target.id !== "per_page") return;

    const perPageSelect = event.target;
    const searchInput = document.getElementById("searchInput");

    const params = new URLSearchParams();

    params.append("q", searchInput.value);
    params.append("per_page", perPageSelect.value);

    cargarUsuarios(`/admin?${params.toString()}`);

}

function manejarClick(event) {

    // ======================================
    // LIMPIAR BÚSQUEDA
    // ======================================

    if (event.target.id === "clearSearch") {

        const searchInput = document.getElementById("searchInput");

        searchInput.value = "";

        const params = new URLSearchParams();

        params.append("q", "");
        params.append("per_page", document.getElementById("per_page").value);

        cargarUsuarios(`/admin?${params.toString()}`);

        return;

    }

    // ======================================
    // PAGINACIÓN AJAX
    // ======================================

    const enlace = event.target.closest("a.page-btn, a.page-number");

    if (enlace) {

        event.preventDefault();
        event.stopPropagation();

        cargarUsuarios(enlace.href);

        return;

    }

    // ======================================
    // ORDENACIÓN COLUMNAS AJAX
    // ======================================

    const ordenar = event.target.closest("th a");

    if (ordenar) {

        event.preventDefault();
        event.stopPropagation();

        cargarUsuarios(ordenar.href);

        return;

    }

}

// ======================================
// AJAX
// ======================================

/**
 * Realiza una petición AJAX al servidor y actualiza
 * el contenido del panel sin recargar la página.
 */
async function cargarUsuarios(url) {

    try {

        const respuesta = await fetch(url, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        if (!respuesta.ok) {
            throw new Error("No fue posible cargar los usuarios.");
        }

        const html = await respuesta.text();

        const contenedor = document.getElementById("users-container");

        contenedor.innerHTML = html;

    } catch (error) {

        console.error(error);

    }

}
