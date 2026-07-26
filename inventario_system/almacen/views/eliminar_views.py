from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from almacen.models import Marca
from almacen.services.configuracion_service import ConfiguracionService

def eliminar_marca(request, pk):

    marca = get_object_or_404(Marca, pk=pk)

    if request.method == "POST":

        ConfiguracionService.eliminar_marca(marca)

        return redirect("lista_marcas")

    return render(
        request,
        "almacen/configuracion/marcas/eliminar.html",
        {
            "marca": marca,
        },
    )