from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from ..forms.ingreso_forms import (
    IngresoNoSerializadoForm,
    RepuestoSerializadoSelectForm,
    UnidadIngresoFormSet, 
)
from ..forms import *
from ..services import *
from ..models import Marca, TipoRepuesto, Repuesto, Modelo, Anaquel
from ..services.inventario_service import InventarioService
from django.core.exceptions import ValidationError
from django.urls import reverse
def ingreso_repuesto(request):
    tipo_ingreso = request.POST.get("tipo_ingreso", "no_serializado")

    form_no_serializado = IngresoNoSerializadoForm(prefix="ns")
    form_repuesto_serializado = RepuestoSerializadoSelectForm(prefix="s")
    formset_unidades = UnidadIngresoFormSet(prefix="unidades")

    if request.method == "POST":
        if tipo_ingreso == "no_serializado":
            form_no_serializado = IngresoNoSerializadoForm(request.POST, prefix="ns")
            if form_no_serializado.is_valid():
                InventarioService.registrar_ingreso_no_serializado(
                    repuesto=form_no_serializado.cleaned_data["repuesto"],
                    cantidad=form_no_serializado.cleaned_data["cantidad"],
                    anaquel_destino=form_no_serializado.cleaned_data["anaquel_destino"],
                    usuario=request.user,
                    observacion=form_no_serializado.cleaned_data["observacion"],
                )
                messages.success(request, "Ingreso registrado correctamente.")
                return redirect("ingreso_repuesto")

        else:  # serializado
            form_repuesto_serializado = RepuestoSerializadoSelectForm(request.POST, prefix="s")
            formset_unidades = UnidadIngresoFormSet(request.POST, request.FILES, prefix="unidades")

            if form_repuesto_serializado.is_valid() and formset_unidades.is_valid():
                unidades_data = [
                    f.cleaned_data for f in formset_unidades
                    if f.cleaned_data and not f.cleaned_data.get("DELETE")
                ]
                InventarioService.registrar_ingreso_serializado(
                    repuesto=form_repuesto_serializado.cleaned_data["repuesto"],
                    unidades_data=unidades_data,
                    usuario=request.user,
                )
                messages.success(request, "Unidades ingresadas correctamente.")
                return redirect("ingreso_repuesto")

    context = {
        "form_no_serializado": form_no_serializado,
        "form_repuesto_serializado": form_repuesto_serializado,
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
        "repuestos": repuestos_pagina,  # ahora es un Page, no el queryset crudo
        "marcas": Marca.objects.all(),
        "tipos": TipoRepuesto.objects.all(),
        "marca_id": marca_id,
        "tipo_id": tipo_id,
        "busqueda": busqueda,
        "breadcrumbs": [("Repuestos", None)],
    }
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
    form = RepuestoForm(request.POST or None, instance=repuesto)
    if request.method == "POST" and form.is_valid():
        InventarioService.actualizar_repuesto(repuesto, form.cleaned_data)
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
    return render(request, "almacen/inventario/repuesto_confirm_delete.html", {"repuesto": repuesto})

#--Buscar por codigo de barras
def buscar_por_codigo(request):
    codigo = request.GET.get("codigo", "").strip()
   
    if not codigo:
        messages.error(request, "Debes ingresar o escanear un código.")
        return redirect("repuesto_list")
    codigo = codigo.upper()  # Convertir a mayúsculas para la búsqueda
    tipo, objeto = InventarioService.buscar_por_codigo(codigo)

    if tipo == "unidad":
        return redirect("unidad_detail", pk=objeto.pk)
    if tipo == "repuesto":
        return redirect("repuesto_detail", pk=objeto.pk)

    messages.error(request, f"No se encontró ningún repuesto o unidad con el código '{codigo}'.")
    return redirect("repuesto_list")