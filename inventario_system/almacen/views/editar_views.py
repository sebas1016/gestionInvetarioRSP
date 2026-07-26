from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

from almacen.forms.marca_forms import MarcaForm
from almacen.models import Marca
from almacen.services.configuracion_service import ConfiguracionService

def editar_marca(request, pk):

    marca = get_object_or_404(Marca, pk=pk)

    form = MarcaForm(
        request.POST or None,
        instance=marca,
    )

    if request.method == "POST":

        if ConfiguracionService.actualizar_marca(form):

            return redirect("lista_marcas")

    return render(
        request,
        "almacen/configuracion/marcas/formulario.html",
        {
            "form": form,
        },
    )