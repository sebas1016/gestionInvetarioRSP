from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from ..forms.ingreso_forms import (
    IngresoRepuestoForm,
    IngresoNoSerializadoDetalleForm,
    UnidadIngresoFormSet,
)
from urllib.parse import quote
from ..forms import *
from ..services import *
from ..models import Marca, TipoRepuesto, Repuesto, Modelo, Anaquel
from ..services.inventario_service import InventarioService
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.http import JsonResponse

from ..forms.ingreso_forms import (
    IngresoRepuestoForm,
    IngresoNoSerializadoDetalleForm,
    UnidadIngresoFormSet,
)
from ..forms import *
from ..services import *
from ..models import Marca, TipoRepuesto, Repuesto, Modelo, Anaquel, MovimientoInventario
from ..services.inventario_service import InventarioService
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.http import JsonResponse

def ingreso_repuesto(request):
    form_repuesto = IngresoRepuestoForm(request.POST or None)
    form_detalle = IngresoNoSerializadoDetalleForm(prefix="ns")
    formset_unidades = UnidadIngresoFormSet(prefix="unidades")

    if request.method == "POST" and form_repuesto.is_valid():
        repuesto = form_repuesto.cleaned_data["repuesto"]

        # El tipo de ingreso lo decide el propio repuesto (repuesto.tipo.es_serializado),
        # nunca un dato que haya mandado el navegador: así, aunque el JS falle o alguien
        # manipule el formulario, jamás se puede registrar un repuesto serializado como
        # stock por cantidad (o viceversa).
        if repuesto.tipo.es_serializado:
            formset_unidades = UnidadIngresoFormSet(request.POST, request.FILES, prefix="unidades")

            if formset_unidades.is_valid():
                unidades_data = [
                    f.cleaned_data for f in formset_unidades
                    if f.cleaned_data and not f.cleaned_data.get("DELETE")
                ]
                InventarioService.registrar_ingreso_serializado(
                    repuesto=repuesto,
                    unidades_data=unidades_data,
                    usuario=request.user,
                )
                messages.success(request, "Unidades ingresadas correctamente.")
                return redirect("ingreso_repuesto")

        else:
            form_detalle = IngresoNoSerializadoDetalleForm(request.POST, prefix="ns")
            if form_detalle.is_valid():
                InventarioService.registrar_ingreso_no_serializado(
                    repuesto=repuesto,
                    cantidad=form_detalle.cleaned_data["cantidad"],
                    anaquel_destino=form_detalle.cleaned_data["anaquel_destino"],
                    usuario=request.user,
                    observacion=form_detalle.cleaned_data["observacion"],
                )
                messages.success(request, "Ingreso registrado correctamente.")
                return redirect("ingreso_repuesto")

    context = {
        "form_repuesto": form_repuesto,
        "form_detalle": form_detalle,
        "formset_unidades": formset_unidades,
    }
    return render(request, "inventario/ingreso_repuesto.html", context)

def repuesto_list(request):
    marca_id = request.GET.get("marca") or None
    tipo_id = request.GET.get("tipo") or None
    busqueda = request.GET.get("q", "").strip()

    repuestos_qs = InventarioService.listar_repuestos(
        marca_id=marca_id, tipo_id=tipo_id, busqueda=busqueda
    )

    paginator = Paginator(repuestos_qs, 100)  # 100 por página, ajustable
    numero_pagina = request.GET.get("page")
    repuestos_pagina = paginator.get_page(numero_pagina)

    context = {
        "repuestos": repuestos_pagina,
        "marcas": Marca.objects.all(),
        "tipos": TipoRepuesto.objects.all(),
        "marca_id": marca_id,
        "tipo_id": tipo_id,
        "busqueda": busqueda,
        "breadcrumbs": [("Repuestos", None)],
    }

    # Búsqueda en vivo: el JS pide esto mismo por fetch mientras el usuario
    # escribe; en ese caso solo se devuelve la tabla, no la página completa.
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "almacen/partials/_repuesto_tabla.html", context)

    return render(request, "inventario/repuesto_list.html", context)



def repuesto_detail(request, pk):
    repuesto = get_object_or_404(
        Repuesto.objects.select_related("modelo__marca", "tipo"), pk=pk
    )

    context = {"repuesto": repuesto,
               "breadcrumbs": [
                ("Repuestos", reverse("repuesto_list")),
                (str(repuesto), None),
                    ],
                }

    if repuesto.tipo.es_serializado:
        unidades_qs = InventarioService.listar_unidades_de_repuesto(repuesto)
        paginator = Paginator(unidades_qs, 100)  # 100 por página, ajustable
        numero_pagina = request.GET.get("page")
        context["unidades"] = paginator.get_page(numero_pagina)
    else:
        context["movimientos"] = InventarioService.listar_movimientos_de_repuesto(repuesto)
            

    return render(request, "inventario/repuesto_detail.html", context)

#---------- Repuesto CRUD Views ----------

def repuesto_create(request):
    form = RepuestoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        repuesto = InventarioService.crear_repuesto(form.cleaned_data)
        messages.success(request, "Repuesto creado correctamente.")
        return redirect("repuesto_detail", pk=repuesto.pk)
    return render(request, "almacen/inventario/repuesto_form.html", {"form": form, "modo": "crear"})

def repuesto_edit(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    # Se captura ANTES de instanciar el form: al llamar a form.is_valid(),
    # Django ya escribe los datos nuevos sobre esta misma instancia
    # (construct_instance), así que si se captura después, "anterior" y
    # "nuevo" siempre quedarían iguales y nunca se detectaría el cambio.
    codigo_anterior = repuesto.codigo_barras

    form = RepuestoForm(request.POST or None, instance=repuesto)
    if request.method == "POST" and form.is_valid():
        InventarioService.actualizar_repuesto(repuesto, form.cleaned_data, codigo_anterior)
        messages.success(request, "Repuesto actualizado correctamente.")
        return redirect("repuesto_detail", pk=repuesto.pk)
    return render(
        request, "almacen/inventario/repuesto_form.html",
        {"form": form, "modo": "editar", "repuesto": repuesto}
    )


def repuesto_delete(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == "POST":
        try:
            InventarioService.eliminar_repuesto(repuesto)
            messages.success(request, "Repuesto eliminado correctamente.")
            return redirect("repuesto_list")
        except ValidationError as error:
            messages.error(request, error.message)
            return redirect("repuesto_detail", pk=repuesto.pk)

    context = {
        "repuesto": repuesto,
        "total_unidades": repuesto.unidades.count(),
        "total_movimientos": MovimientoInventario.objects.filter(repuesto=repuesto).count(),
    }
    return render(request, "almacen/inventario/repuesto_confirm_delete.html", context)

#--Sugerencia de anaquel para un repuesto (usado en el form de ingreso)
def anaquel_sugerido(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, pk=repuesto_id)
    anaquel = InventarioService.obtener_anaquel_sugerido(repuesto)
    return JsonResponse({
        "anaquel_id": anaquel.pk if anaquel else None,
        "anaquel_codigo": anaquel.codigo if anaquel else None,
    })

#--Buscar por codigo de barras (o, si no coincide con ninguno, busqueda general)
def buscar_por_codigo(request):
    texto = request.GET.get("codigo", "").strip()

    if not texto:
        messages.error(request, "Debes ingresar un texto o código a buscar.")
        return redirect("repuesto_list")

    tipo, objeto = InventarioService.buscar_por_codigo(texto.upper())

    if tipo == "unidad":
        return redirect("unidad_detail", pk=objeto.pk)
    if tipo == "repuesto":
        return redirect("repuesto_detail", pk=objeto.pk)

    # No coincidió con ningún código de barras exacto: se trata como una
    # búsqueda general (marca, modelo, tipo, anaquel, referencia, etc.)
    # y se muestra en el listado de repuestos.
    return redirect(f"{reverse('repuesto_list')}?q={quote(texto)}")

