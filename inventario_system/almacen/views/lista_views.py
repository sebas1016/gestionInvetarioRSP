from django.shortcuts import render

from almacen.models import Marca
from almacen.services.configuracion_service import ConfiguracionService
from core.utils.page import page_context


def lista_marcas(request):

    context = page_context(

        title="Marcas",

        description="Administra las marcas del sistema.",

        marcas=ConfiguracionService.listar_marcas(),

        total=Marca.objects.count(),

    )

    return render(
        request,
        "almacen/configuracion/marcas/lista.html",
        context,
    )