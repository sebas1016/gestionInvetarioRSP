from django import forms
from ..models import Marca, Modelo, TipoRepuesto, Anaquel
from .mixins import BootstrapFormMixin

class MarcaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre"]


class ModeloForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ["marca", "nombre"]


class TipoRepuestoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TipoRepuesto
        fields = ["nombre", "es_serializado"]


class AnaquelForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Anaquel
        fields = ["codigo", "descripcion"]