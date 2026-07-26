from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import UnidadRepuesto, Repuesto
from ..forms.historial_forms import RetiroComponenteForm
from ..services.inventario_service import InventarioService
from django.urls import reverse


def unidad_detail(request, pk):
    unidad = get_object_or_404(
        UnidadRepuesto.objects.select_related("repuesto", "anaquel"), pk=pk
    )

    if request.method == "POST":
        form = RetiroComponenteForm(request.POST, request.FILES)
        if form.is_valid():
            InventarioService.registrar_retiro_componente(
                unidad=unidad, data=form.cleaned_data, usuario=request.user
            )
            return redirect("unidad_detail", pk=unidad.pk)
    else:
        form = RetiroComponenteForm()

    context = {
        "unidad": unidad,
        "fotos": unidad.fotos.all(),  # ya viene ordenado -version por Meta.ordering
        "componentes": unidad.componentes.order_by("-fecha"),
        "form": form,
        "breadcrumbs": [
            ("Repuestos", reverse("repuesto_list")),
            (str(unidad.repuesto), reverse("repuesto_detail", args=[unidad.repuesto.pk])),
            (unidad.codigo_unico, None),],
    }
    return render(request, "inventario/unidad_detail.html", context)

def unidad_etiqueta(request, pk):
    unidad = get_object_or_404(
        UnidadRepuesto.objects.select_related("repuesto", "anaquel"), pk=pk
    )
    return render(request, "almacen/inventario/unidad_etiqueta.html", {"unidad": unidad})

def repuesto_etiqueta(request, pk):
    repuesto = get_object_or_404(
        Repuesto.objects.select_related("modelo__marca", "tipo"), pk=pk
    )
    return render(request, "almacen/inventario/repuesto_etiqueta.html", {"repuesto": repuesto})