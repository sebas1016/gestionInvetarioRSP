from django.shortcuts import render
from .models.repuesto import Repuesto


def lista_repuestos(request):

    busqueda=request.GET.get(
        'buscar',
        ''
    )

    repuestos=Repuesto.objects.all()

    if busqueda:

        repuestos=repuestos.filter(
            referencia__icontains=busqueda
        )

    contexto={

        'repuestos':repuestos

    }

    return render(
        request,
        'inventario/lista_repuestos.html',
        contexto
    )