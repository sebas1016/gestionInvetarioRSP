from django.shortcuts import render,redirect
from ..forms.movimiento_form import MovimientoForm
from ..services.inventario_service import (
    InventarioService
)
from core.utils.page import page_context
from django.contrib import messages
from django.core.exceptions import ValidationError
from ..services.movimiento_service import MovimientoService
from ..forms.movimiento_form import SalidaNoSerializadoForm, SalidaSerializadoForm
from django.core.paginator import Paginator

def crear_movimiento(request):

    form=MovimientoForm()

    if request.method=="POST":

        form=MovimientoForm(
            request.POST
        )

        if form.is_valid():

            datos=form.cleaned_data

            if datos['tipo']=="ENTRADA":
                print(datos['anaquel'])
                InventarioService.entrada(

                    repuesto=datos['repuesto'],
                    cantidad=datos['cantidad'],
                    usuario=request.user,
                    anaquel=datos['anaquel'],
                    observacion=datos['observacion']

                )

            else:

                InventarioService.salida(

                    repuesto=datos['repuesto'],
                    cantidad=datos['cantidad'],
                    unidad=datos['unidad'],
                    usuario=request.user,
                    observacion=datos['observacion']
                )

            return redirect(
                'lista_repuestos'
            )
    
    context = page_context(

        title="Movimientos",

        description="Registra entradas y salidas del inventario.",

        breadcrumbs=[

            {

                "title":"Inicio",

                "url":"dashboard"

            },

            {

                "title":"Movimientos",

                "url":None

            }

        ],

        action={

            "title":"Nuevo Movimiento",

            "url":"movimientos:crear",

            "icon":"bi-plus-circle"

        }

    )

    return render(

        request,
        'inventario/movimiento.html',
        {'form':form},
        context
    )

#Moviemiento de Salida

def salida(request):
    codigo = request.GET.get("codigo", "").strip() or request.POST.get("codigo", "").strip()

    tipo_encontrado = None
    objeto_encontrado = None
    form = None

    if codigo:
        codigo = codigo
        tipo_encontrado, objeto_encontrado = InventarioService.buscar_por_codigo(codigo)

        if tipo_encontrado is None:
            messages.error(request, f"No se encontró ningún repuesto o unidad con el código '{codigo}'.")

    if request.method == "POST" and tipo_encontrado:
        if tipo_encontrado == "repuesto":
            form = SalidaNoSerializadoForm(request.POST)
            if form.is_valid():
                try:
                    MovimientoService.registrar_salida_no_serializado(
                        repuesto=objeto_encontrado,
                        cantidad=form.cleaned_data["cantidad"],
                        anaquel_origen=form.cleaned_data["anaquel_origen"],
                        usuario=request.user,
                        observacion=form.cleaned_data["observacion"],
                    )
                    messages.success(request, "Salida registrada correctamente.")
                    return redirect("salida")
                except ValidationError as error:
                    messages.error(request, error.message)

        else:  # unidad
            form = SalidaSerializadoForm(request.POST)
            if form.is_valid():
                MovimientoService.registrar_salida_serializada(
                    unidad=objeto_encontrado,
                    nuevo_estado=form.cleaned_data["nuevo_estado"],
                    usuario=request.user,
                    observacion=form.cleaned_data["observacion"],
                )
                messages.success(request, "Salida registrada correctamente.")
                return redirect("salida")

    elif tipo_encontrado == "repuesto":
        anaquel_sugerido = InventarioService.obtener_anaquel_sugerido(objeto_encontrado)
        form = SalidaNoSerializadoForm(
            initial={"anaquel_origen": anaquel_sugerido} if anaquel_sugerido else None
        )
    elif tipo_encontrado == "unidad":
        form = SalidaSerializadoForm()

    context = {
        "codigo": codigo,
        "tipo_encontrado": tipo_encontrado,
        "objeto_encontrado": objeto_encontrado,
        "form": form,
    }
    return render(request, "almacen/inventario/salida.html", context)

    

def movimiento_list(request):
    tipo = request.GET.get("tipo") or None
    busqueda = request.GET.get("q", "").strip()
    fecha_desde = request.GET.get("desde") or None
    fecha_hasta = request.GET.get("hasta") or None

    movimientos_qs = MovimientoService.listar_movimientos(
        tipo=tipo, busqueda=busqueda, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta
    )

    paginator = Paginator(movimientos_qs, 25)
    numero_pagina = request.GET.get("page")
    movimientos_pagina = paginator.get_page(numero_pagina)

    context = {
        "movimientos": movimientos_pagina,
        "tipo": tipo,
        "busqueda": busqueda,
        "fecha_desde": fecha_desde or "",
        "fecha_hasta": fecha_hasta or "",
    }
    return render(request, "almacen/inventario/movimiento_list.html", context)