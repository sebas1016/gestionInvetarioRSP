from django.shortcuts import redirect, render

from almacen.forms.marca_forms import MarcaForm
from almacen.services.configuracion_service import ConfiguracionService


def crear_marca(request):

    form = MarcaForm(request.POST or None)

    if request.method == "POST":

        if ConfiguracionService.crear_marca(form):

            return redirect("lista_marcas")

    return render(
        request,
        "almacen/configuracion/marcas/formulario.html",
        {
            "form": form,
        },
    )