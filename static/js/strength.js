document.querySelectorAll(".strength-password").forEach((passwordField) => {

    const strengthText =
        passwordField.parentElement.nextElementSibling;

    if (!strengthText) return;

    passwordField.addEventListener("input", () => {

        const password = passwordField.value;

        let score = 0;

        if (password.length >= 8) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

        if (password.length === 0) {

            strengthText.textContent = "";
            strengthText.style.color = "";

        } else if (score <= 2) {

            strengthText.textContent = "🔴 Contraseña débil";
            strengthText.style.color = "#ef4444";

        } else if (score <= 4) {

            strengthText.textContent = "🟡 Contraseña media";
            strengthText.style.color = "#f59e0b";

        } else {

            strengthText.textContent = "🟢 Contraseña fuerte";
            strengthText.style.color = "#22c55e";

        }

    });

});