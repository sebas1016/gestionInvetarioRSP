document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("app-sidebar");
    const toggle = document.getElementById("sidebar-toggle");

    if (toggle) {
        toggle.addEventListener("click", function () {
            sidebar.classList.toggle("is-open");
        });
    }
});