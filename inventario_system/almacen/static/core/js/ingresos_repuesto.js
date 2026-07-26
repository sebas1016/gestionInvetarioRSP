document.addEventListener("DOMContentLoaded", function () {
    const optNoSerializado = document.getElementById("opt-no-serializado");
    const optSerializado = document.getElementById("opt-serializado");
    const formNoSerializado = document.getElementById("form-no-serializado");
    const formSerializado = document.getElementById("form-serializado");

    function actualizarVisibilidad() {
        if (optSerializado.checked) {
            formNoSerializado.classList.add("d-none");
            formSerializado.classList.remove("d-none");
        } else {
            formSerializado.classList.add("d-none");
            formNoSerializado.classList.remove("d-none");
        }
    }

    optNoSerializado.addEventListener("change", actualizarVisibilidad);
    optSerializado.addEventListener("change", actualizarVisibilidad);
    actualizarVisibilidad();

    // ---- Formset dinámico de unidades ----
    const container = document.getElementById("unidades-container");
    const totalFormsInput = document.querySelector("#id_unidades-TOTAL_FORMS");
    const emptyTemplate = document.getElementById("unidad-empty-template");
    const btnAgregar = document.getElementById("btn-agregar-unidad");

    btnAgregar.addEventListener("click", function () {
        const formIndex = parseInt(totalFormsInput.value, 10);
        const html = emptyTemplate.innerHTML.replace(/__prefix__/g, formIndex);

        const wrapper = document.createElement("div");
        wrapper.innerHTML = html.trim();
        container.appendChild(wrapper.firstElementChild);

        totalFormsInput.value = formIndex + 1;
    });

    container.addEventListener("click", function (event) {
        if (event.target.classList.contains("btn-quitar-unidad")) {
            event.target.closest(".unidad-bloque").remove();
            // Nota: no se reindexan los forms restantes; Django tolera huecos
            // en los índices siempre y cuando TOTAL_FORMS sea >= al índice más alto presente.
        }
    });
});