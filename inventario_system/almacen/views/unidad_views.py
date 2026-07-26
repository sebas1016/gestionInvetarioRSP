from django.shortcuts import (
    render,
    get_object_or_404
)

from ..models.unidad_repuesto import (
    UnidadRepuesto
)

from ..models.movimiento import (
    MovimientoInventario
)


def detalle_unidad(
    request,
    unidad_id
):

    unidad=get_object_or_404(

        UnidadRepuesto.objects.select_related(
            'repuesto',
            'repuesto__modelo__marca',
            'repuesto__modelo'
        ),

        id=unidad_id
    )

    movimientos=(

        MovimientoInventario.objects

        .filter(
            unidad=unidad
        )

        .select_related(
            'usuario',
            'anaquel_origen',
            'anaquel_destino'
        )

        .order_by(
            '-fecha'
        )

    )

    contexto={

        'unidad':unidad,
        'movimientos':movimientos

    }

    return render(

        request,

        'inventario/detalle_unidad.html',

        contexto
    )