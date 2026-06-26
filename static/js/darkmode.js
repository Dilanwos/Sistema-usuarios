// Aplicar el tema guardado al cargar la página
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
}

// Botón para cambiar el tema
const themeButton = document.getElementById("theme-toggle");

if (themeButton) {

    themeButton.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }

    });

}