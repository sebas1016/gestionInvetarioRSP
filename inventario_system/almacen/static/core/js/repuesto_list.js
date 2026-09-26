document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-filtro-repuestos");
    const input = document.getElementById("input-busqueda-repuestos");
    const contenedor = document.getElementById("repuesto-tabla-contenedor");

    if (!form || !contenedor) return;

    let temporizador = null;

    function construirUrl(paginaOverride) {
        const datos = new FormData(form);
        const params = new URLSearchParams();
        for (const [clave, valor] of datos.entries()) {
            if (valor) params.set(clave, valor);
        }
        if (paginaOverride) {
            params.set("page", paginaOverride);
        }
        return `${form.action}?${params.toString()}`;
    }

    function cargarTabla(url, actualizarHistorial) {
        fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then((resp) => (resp.ok ? resp.text() : null))
            .then((html) => {
                if (html === null) return;
                contenedor.innerHTML = html;
                if (actualizarHistorial) {
                    window.history.replaceState(null, "", url);
                }
            })
            .catch(() => {
                // Si falla la búsqueda en vivo, no se rompe nada: el botón
                // "Filtrar" de toda la vida sigue funcionando normal.
            });
    }

    // Busca mientras se escribe, con un pequeño retraso para no mandar
    // una petición por cada tecla presionada.
    if (input) {
        input.addEventListener("input", function () {
            clearTimeout(temporizador);
            temporizador = setTimeout(function () {
                cargarTabla(construirUrl());
            }, 350);
        });
    }

    // Cambiar marca o tipo filtra al instante, sin esperar.
    form.querySelectorAll("select").forEach((select) => {
        select.addEventListener("change", function () {
            clearTimeout(temporizador);
            cargarTabla(construirUrl());
        });
    });

    // El botón "Filtrar" sigue ahí (por si JS falla) pero ahora tampoco recarga la página.
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        clearTimeout(temporizador);
        cargarTabla(construirUrl());
    });

    // Los links "Anterior"/"Siguiente" se regeneran dentro del contenedor
    // cada vez que se recarga la tabla, así que se escuchan ahí (delegación).
    contenedor.addEventListener("click", function (event) {
        const link = event.target.closest(".page-link[href]");
        if (!link) return;
        event.preventDefault();
        cargarTabla(link.getAttribute("href"));
    });
});