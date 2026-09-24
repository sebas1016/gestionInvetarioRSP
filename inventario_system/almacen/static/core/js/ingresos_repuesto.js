document.addEventListener("DOMContentLoaded", function () {
    const selectRepuesto = document.getElementById("id_repuesto");
    const formNoSerializado = document.getElementById("form-no-serializado");
    const formSerializado = document.getElementById("form-serializado");

    // ---- Cuadro de búsqueda integrado en el select de repuesto ----
    attachSearchableSelect(selectRepuesto, { placeholder: "Buscar repuesto..." });

    // ---- Cuadro de búsqueda en el anaquel del form no-serializado ----
    attachSearchableSelect("id_ns-anaquel_destino", { placeholder: "Buscar anaquel..." });

    // ---- Cuadro de búsqueda en los anaqueles de unidades serializadas ----
    function initBusquedaAnaquelesUnidades(scope) {
        const raiz = scope || document;
        raiz.querySelectorAll('select[id^="id_unidades-"][id$="-anaquel"]').forEach((select) => {
            attachSearchableSelect(select, { placeholder: "Buscar anaquel..." });
        });
    }
    initBusquedaAnaquelesUnidades(document);

    // ---- Mostrar automáticamente el panel que corresponde según el repuesto elegido ----
    // Cada <option> del select trae data-serializado="true"/"false" (ver
    // RepuestoConTipoSelect en forms/ingreso_forms.py), así el navegador no
    // necesita preguntarle nada al usuario: ya sabe qué tipo de repuesto es.
    function actualizarPanelSegunRepuesto() {
        const opcion = selectRepuesto.options[selectRepuesto.selectedIndex];
        const esSerializado = opcion ? opcion.dataset.serializado : undefined;

        if (esSerializado === "true") {
            formSerializado.classList.remove("d-none");
            formNoSerializado.classList.add("d-none");
            selectRepuesto.setAttribute("form", "form-serializado");
        } else if (esSerializado === "false") {
            formNoSerializado.classList.remove("d-none");
            formSerializado.classList.add("d-none");
            selectRepuesto.setAttribute("form", "form-no-serializado");
        } else {
            // Sin repuesto elegido todavía: no se muestra ningún panel.
            formNoSerializado.classList.add("d-none");
            formSerializado.classList.add("d-none");
            selectRepuesto.removeAttribute("form");
        }
    }

    selectRepuesto.addEventListener("change", actualizarPanelSegunRepuesto);
    actualizarPanelSegunRepuesto(); // por si vuelve con errores de validación y un repuesto ya elegido

    // ---- Auto-selección del anaquel destino según el último ingreso del repuesto ----
    const cardIngreso = document.querySelector(".ingreso-card");
    const urlTemplate = cardIngreso ? cardIngreso.dataset.anaquelSugeridoUrl : null;

    function urlSugerenciaPara(repuestoId) {
        if (!urlTemplate) return null;
        return urlTemplate.replace(/999999\/$/, repuestoId + "/");
    }

    function aplicarAnaquelSugerido(repuestoId, aplicarCallback) {
        const url = urlSugerenciaPara(repuestoId);
        if (!repuestoId || !url) return;

        fetch(url)
            .then((resp) => (resp.ok ? resp.json() : null))
            .then((data) => {
                if (data && data.anaquel_id) {
                    aplicarCallback(String(data.anaquel_id));
                }
            })
            .catch(() => {
                // Si falla la sugerencia, simplemente se deja la selección manual.
            });
    }

    // Cambia el valor de un <select> de anaquel y avisa al combo con
    // búsqueda (si lo tiene) para que actualice el texto visible.
    function fijarValorAnaquel(select, anaquelId) {
        select.value = anaquelId;
        select.dispatchEvent(new Event("change", { bubbles: true }));
    }

    const selectAnaquelDestino = document.getElementById("id_ns-anaquel_destino");
    let anaquelSugeridoActual = null;

    function aplicarSugerenciaAUnidadesVisibles() {
        if (!anaquelSugeridoActual) return;
        document.querySelectorAll('select[id^="id_unidades-"][id$="-anaquel"]').forEach((select) => {
            fijarValorAnaquel(select, anaquelSugeridoActual);
        });
    }

    selectRepuesto.addEventListener("change", function () {
        const repuestoId = this.value;
        anaquelSugeridoActual = null;

        aplicarAnaquelSugerido(repuestoId, function (anaquelId) {
            anaquelSugeridoActual = anaquelId;

            if (selectAnaquelDestino) {
                fijarValorAnaquel(selectAnaquelDestino, anaquelId);
            }
            aplicarSugerenciaAUnidadesVisibles();
        });
    });

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
        const nuevoBloque = wrapper.firstElementChild;
        container.appendChild(nuevoBloque);

        totalFormsInput.value = formIndex + 1;

        // Activa el cuadro de búsqueda en el anaquel del bloque recién creado.
        initBusquedaAnaquelesUnidades(nuevoBloque);

        // Si ya hay un anaquel sugerido para el repuesto elegido, se aplica
        // también a la unidad recién agregada.
        aplicarSugerenciaAUnidadesVisibles();
    });

    container.addEventListener("click", function (event) {
        if (event.target.classList.contains("btn-quitar-unidad")) {
            event.target.closest(".unidad-bloque").remove();
        }
    });
});