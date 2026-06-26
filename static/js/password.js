document.querySelectorAll(".password-container").forEach((container) => {

    const input = container.querySelector(".password-input");
    const button = container.querySelector(".toggle-password");

    if (!input || !button) return;

    button.style.display = "none";

    input.addEventListener("input", () => {

        button.style.display =
            input.value.length > 0
                ? "flex"
                : "none";

    });

    button.addEventListener("click", (e) => {

        e.preventDefault();

        input.type =
            input.type === "password"
                ? "text"
                : "password";

        button.textContent =
            input.type === "password"
                ? "👁️"
                : "🙈";

    });

});