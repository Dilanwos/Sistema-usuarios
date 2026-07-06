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

    // ======================================
    // ABRIR MODAL ELIMINAR
    // ======================================

    const botonEliminar = event.target.closest(
        '[data-action="delete-user"]'
    );

    if (botonEliminar) {

        event.preventDefault();

        abrirModalEliminar(botonEliminar);

        return;

    }

    // ======================================
    // CONFIRMAR ELIMINACIÓN AJAX
    // ======================================

    if (event.target.id === "confirmDelete") {

    eliminarUsuario(event.target.dataset.url);

    return;

    }
}

/**
 * Abre el modal de confirmación para eliminar un usuario.
 */
function abrirModalEliminar(boton) {

    console.log(boton);
    console.log(boton.dataset);

    const modal = document.getElementById("deleteModal");

    document.getElementById("usuarioNombre").textContent =
        boton.dataset.nombre;

    document.getElementById("usuarioEmail").textContent =
        boton.dataset.email;

    document.getElementById("usuarioRol").textContent =
        boton.dataset.rol;

    document.getElementById("confirmDelete").dataset.url =
        boton.href;

    modal.style.display = "flex";

}

/**
 * Elimina un usuario mediante una petición AJAX.
 */
async function eliminarUsuario(url) {

    try {

        const respuesta = await fetch(url, {

            method: "POST",

            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }

        });

        const resultado = await respuesta.json();

        if (!resultado.success) {

            throw new Error(resultado.message);

        }

        cerrarModal();

        cargarUsuarios(window.location.href);

    } catch (error) {

        console.error(error);

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
