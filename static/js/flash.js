document.addEventListener("DOMContentLoaded", () => {

    const flashes =
        document.querySelectorAll(".auto-hide");

    flashes.forEach((flash) => {

        setTimeout(() => {

            flash.classList.add("hide");

            setTimeout(() => {

                flash.remove();

            }, 500);

        }, 4000);

    });

});