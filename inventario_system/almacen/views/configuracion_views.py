from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from ..models import Marca, Modelo, TipoRepuesto, Anaquel
from ..forms.configuracion_forms import (
    MarcaForm, ModeloForm, TipoRepuestoForm, AnaquelForm
)
from ..services.configuracion_service import ConfiguracionService


# ---------------- Marca ----------------

def marca_list(request):
    if request.method == "POST":
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Marca creada correctamente.")
            return redirect("marca_list")
    else:
        form = MarcaForm()

    context = {"marcas": Marca.objects.all().order_by("nombre"), "form": form}
    return render(request, "almacen/configuracion/marca_list.html", context)


def marca_edit(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    form = MarcaForm(request.POST or None, instance=marca)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Marca actualizada correctamente.")
        return redirect("marca_list")
    return render(request, "almacen/configuracion/marca_edit.html", {"form": form, "marca": marca})



def marca_delete(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == "POST":
        try:
            ConfiguracionService.eliminar(
                marca, "No se puede eliminar la marca porque tiene modelos asociados."
            )
            messages.success(request, "Marca eliminada correctamente.")
        except ValidationError as error:
            messages.error(request, error.message)
        return redirect("marca_list")
    return render(request, "almacen/configuracion/marca_confirm_delete.html", {"marca": marca})

# ---------------- Modelo ----------------

def modelo_list(request):
    if request.method == "POST":
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Modelo creado correctamente.")
            return redirect("modelo_list")
    else:
        form = ModeloForm()

    context = {
        "modelos": Modelo.objects.select_related("marca").order_by("marca__nombre", "nombre"),
        "form": form,
    }
    return render(request, "almacen/configuracion/modelo_list.html", context)

def modelo_edit(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)
    form = ModeloForm(request.POST or None, instance=modelo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Modelo actualizado correctamente.")
        return redirect("modelo_list")
    return render(request, "almacen/configuracion/modelo_edit.html", {"form": form, "modelo": modelo})


def modelo_delete(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)
    if request.method == "POST":
        try:
            ConfiguracionService.eliminar(
                modelo, "No se puede eliminar el modelo porque tiene repuestos asociados."
            )
            messages.success(request, "Modelo eliminado correctamente.")
        except ValidationError as error:
            messages.error(request, error.message)
        return redirect("modelo_list")
    return render(request, "almacen/configuracion/modelo_confirm_delete.html", {"modelo": modelo})


# ---------------- TipoRepuesto ----------------

def tipo_list(request):
    if request.method == "POST":
        form = TipoRepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo creado correctamente.")
            return redirect("tipo_list")
    else:
        form = TipoRepuestoForm()

    context = {"tipos": TipoRepuesto.objects.all().order_by("nombre"), "form": form}
    return render(request, "almacen/configuracion/tipo_list.html", context)


def tipo_edit(request, pk):
    tipo = get_object_or_404(TipoRepuesto, pk=pk)
    form = TipoRepuestoForm(request.POST or None, instance=tipo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tipo actualizado correctamente.")
        return redirect("tipo_list")
    return render(request, "almacen/configuracion/tipo_edit.html", {"form": form, "tipo": tipo})


def tipo_delete(request, pk):
    tipo = get_object_or_404(TipoRepuesto, pk=pk)
    if request.method == "POST":
        try:
            ConfiguracionService.eliminar(
                tipo, "No se puede eliminar el tipo porque tiene repuestos asociados."
            )
            messages.success(request, "Tipo eliminado correctamente.")
        except ValidationError as error:
            messages.error(request, error.message)
        return redirect("tipo_list")
    return render(request, "almacen/configuracion/tipo_confirm_delete.html", {"tipo": tipo})


# ---------------- Anaquel ----------------

def anaquel_list(request):
    if request.method == "POST":
        form = AnaquelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Anaquel creado correctamente.")
            return redirect("anaquel_list")
    else:
        form = AnaquelForm()

    context = {"anaqueles": Anaquel.objects.all().order_by("codigo"), "form": form}
    return render(request, "almacen/configuracion/anaquel_list.html", context)


def anaquel_edit(request, pk):
    anaquel = get_object_or_404(Anaquel, pk=pk)
    form = AnaquelForm(request.POST or None, instance=anaquel)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Anaquel actualizado correctamente.")
        return redirect("anaquel_list")
    return render(request, "almacen/configuracion/anaquel_edit.html", {"form": form, "anaquel": anaquel})


def anaquel_delete(request, pk):
    anaquel = get_object_or_404(Anaquel, pk=pk)
    if request.method == "POST":
        try:
            ConfiguracionService.eliminar(
                anaquel, "No se puede eliminar el anaquel porque tiene unidades o movimientos asociados."
            )
            messages.success(request, "Anaquel eliminado correctamente.")
        except ValidationError as error:
            messages.error(request, error.message)
        return redirect("anaquel_list")
    return render(request, "almacen/configuracion/anaquel_confirm_delete.html", {"anaquel": anaquel})