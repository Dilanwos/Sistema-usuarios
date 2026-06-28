const searchInput = document.getElementById("searchInput");
const searchForm = document.getElementById("searchForm");

if (searchInput && searchForm) {

    let timeout;

    searchInput.addEventListener("input", () => {

        clearTimeout(timeout);

        timeout = setTimeout(() => {

            searchForm.submit();

        }, 300);

    });

}

const perPageSelect = document.getElementById("per_page");
const currentPerPage = document.getElementById("currentPerPage");

if (perPageSelect && currentPerPage) {
    perPageSelect.value = currentPerPage.value;
}

const clearButton = document.getElementById("clearSearch");

if (searchInput && clearButton) {

    function updateClearButton() {
    clearButton.style.display = "flex";
    }

    updateClearButton();

    searchInput.addEventListener("input", updateClearButton);

    clearButton.addEventListener("click", () => {

        searchInput.value = "";

        searchForm.submit();

    });

}