/**
 * Convierte un <select> nativo en un combo con cuadro de búsqueda integrado,
 * sin depender de ninguna librería externa (no requiere CDN ni internet).
 *
 * El <select> original se mantiene en el DOM (oculto) para que el formulario
 * se siga enviando exactamente igual que antes, y se dispara un evento
 * "change" nativo sobre él cada vez que se elige una opción, para que el
 * resto del código (por ejemplo, la sugerencia automática de anaquel) siga
 * funcionando sin cambios.
 *
 * Uso: attachSearchableSelect("id_ns-repuesto", { placeholder: "Buscar..." })
 */
function attachSearchableSelect(elementOrId, opciones) {
    const config = Object.assign({
        placeholder: "Buscar...",
        noResultsText: "Sin resultados",
    }, opciones || {});

    const select = typeof elementOrId === "string"
        ? document.getElementById(elementOrId)
        : elementOrId;

    if (!select || select.dataset.searchableInit === "1") {
        return null;
    }
    select.dataset.searchableInit = "1";

    // ---- Construcción del wrapper ----
    const wrapper = document.createElement("div");
    wrapper.className = "ss-wrapper";

    const input = document.createElement("input");
    input.type = "text";
    input.className = "form-control ss-input";
    input.autocomplete = "off";
    input.placeholder = config.placeholder;

    const dropdown = document.createElement("div");
    dropdown.className = "ss-dropdown d-none";

    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(input);
    wrapper.appendChild(dropdown);
    wrapper.appendChild(select);
    select.classList.add("ss-native-select");

    function opcionesDisponibles() {
        return Array.from(select.options).filter((opt) => opt.value !== "");
    }

    function textoSeleccionActual() {
        const seleccionada = select.options[select.selectedIndex];
        return seleccionada && seleccionada.value !== "" ? seleccionada.text : "";
    }

    function renderDropdown(filtro) {
        const texto = (filtro || "").toLowerCase();
        dropdown.innerHTML = "";

        const coincidencias = opcionesDisponibles().filter((opt) =>
            opt.text.toLowerCase().includes(texto)
        );

        if (coincidencias.length === 0) {
            const vacio = document.createElement("div");
            vacio.className = "ss-item ss-item--empty";
            vacio.textContent = config.noResultsText;
            dropdown.appendChild(vacio);
            return;
        }

        coincidencias.forEach((opt) => {
            const item = document.createElement("div");
            item.className = "ss-item";
            item.textContent = opt.text;
            if (opt.value === select.value) {
                item.classList.add("is-active");
            }
            item.addEventListener("mousedown", function (event) {
                // mousedown en vez de click: se dispara antes que el blur del input
                event.preventDefault();
                seleccionar(opt);
            });
            dropdown.appendChild(item);
        });
    }

    function seleccionar(opt) {
        select.value = opt.value;
        input.value = opt.text;
        cerrarDropdown();
        select.dispatchEvent(new Event("change", { bubbles: true }));
    }

    function abrirDropdown() {
        renderDropdown("");
        dropdown.classList.remove("d-none");
    }

    function cerrarDropdown() {
        dropdown.classList.add("d-none");
    }

    // Estado inicial: refleja la opción ya seleccionada del <select>
    input.value = textoSeleccionActual();

    // Si algo externo cambia el valor del <select> (por ejemplo, la
    // sugerencia automática de anaquel) y dispara un evento "change",
    // el texto visible del combo se mantiene sincronizado.
    select.addEventListener("change", function () {
        input.value = textoSeleccionActual();
    });
    
    input.addEventListener("focus", function () {
        input.value = "";
        abrirDropdown();
    });

    input.addEventListener("input", function () {
        renderDropdown(input.value);
        dropdown.classList.remove("d-none");
    });

    input.addEventListener("blur", function () {
        // Pequeño retraso para permitir que el mousedown del item se procese antes.
        setTimeout(function () {
            input.value = textoSeleccionActual();
            cerrarDropdown();
        }, 150);
    });

    input.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            input.value = textoSeleccionActual();
            cerrarDropdown();
            input.blur();
        }
    });

    document.addEventListener("click", function (event) {
        if (!wrapper.contains(event.target)) {
            cerrarDropdown();
        }
    });

    return {
        setValue: function (value) {
            const opt = opcionesDisponibles().find((o) => o.value === String(value));
            if (opt) {
                seleccionar(opt);
            }
        },
    };
}