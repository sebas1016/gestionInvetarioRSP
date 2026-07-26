from django import forms
from django.forms import formset_factory

from ..models import Repuesto, Anaquel
from .mixins import BootstrapFormMixin


class IngresoNoSerializadoForm(BootstrapFormMixin, forms.Form):
    repuesto = forms.ModelChoiceField(queryset=Repuesto.objects.filter(tipo__es_serializado=False))
    cantidad = forms.IntegerField(min_value=1)
    anaquel_destino = forms.ModelChoiceField(queryset=Anaquel.objects.all())
    observacion = forms.CharField(widget=forms.Textarea, required=False)


class UnidadIngresoForm(BootstrapFormMixin, forms.Form):
    anaquel = forms.ModelChoiceField(queryset=Anaquel.objects.all())
    foto_frontal = forms.ImageField()
    foto_trasera = forms.ImageField()
    observacion = forms.CharField(widget=forms.Textarea, required=False)


UnidadIngresoFormSet = formset_factory(UnidadIngresoForm, extra=1, can_delete=True)

class RepuestoSerializadoSelectForm(BootstrapFormMixin, forms.Form):
    repuesto = forms.ModelChoiceField(queryset=Repuesto.objects.filter(tipo__es_serializado=True))