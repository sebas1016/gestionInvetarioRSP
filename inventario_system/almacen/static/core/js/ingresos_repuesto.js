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

    // ---- Cuadro de búsqueda integrado en los selects de repuesto ----
    attachSearchableSelect("id_ns-repuesto", { placeholder: "Buscar repuesto..." });
    attachSearchableSelect("id_s-repuesto", { placeholder: "Buscar repuesto..." });

    // ---- Cuadro de búsqueda integrado en el select de anaquel (no serializado) ----
    attachSearchableSelect("id_ns-anaquel_destino", { placeholder: "Buscar anaquel..." });

    // ---- Cuadro de búsqueda en los anaqueles de unidades serializadas ----
    function initBusquedaAnaquelesUnidades(scope) {
        const raiz = scope || document;
        raiz.querySelectorAll('select[id^="id_unidades-"][id$="-anaquel"]').forEach((select) => {
            attachSearchableSelect(select, { placeholder: "Buscar anaquel..." });
        });
    }
    initBusquedaAnaquelesUnidades(document);

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

    // -- Repuesto con stock (no serializado): selecciona anaquel_destino --
    const selectRepuestoNS = document.getElementById("id_ns-repuesto");
    const selectAnaquelDestino = document.getElementById("id_ns-anaquel_destino");

    if (selectRepuestoNS && selectAnaquelDestino) {
        selectRepuestoNS.addEventListener("change", function () {
            aplicarAnaquelSugerido(this.value, function (anaquelId) {
                fijarValorAnaquel(selectAnaquelDestino, anaquelId);
            });
        });
    }

    // -- Unidades serializadas: sugiere el anaquel de cada unidad nueva --
    const selectRepuestoS = document.getElementById("id_s-repuesto");
    let anaquelSugeridoSerializado = null;

    function aplicarSugerenciaAUnidadesVisibles() {
        if (!anaquelSugeridoSerializado) return;
        document.querySelectorAll('select[id^="id_unidades-"][id$="-anaquel"]').forEach((select) => {
            fijarValorAnaquel(select, anaquelSugeridoSerializado);
        });
    }

    if (selectRepuestoS) {
        selectRepuestoS.addEventListener("change", function () {
            const repuestoId = this.value;
            aplicarAnaquelSugerido(repuestoId, function (anaquelId) {
                anaquelSugeridoSerializado = anaquelId;
                aplicarSugerenciaAUnidadesVisibles();
            });
        });
    }

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
            // Nota: no se reindexan los forms restantes; Django tolera huecos
            // en los índices siempre y cuando TOTAL_FORMS sea >= al índice más alto presente.
        }
    });
});