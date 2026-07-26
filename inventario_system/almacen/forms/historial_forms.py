from django import forms
from .mixins import BootstrapFormMixin

class RetiroComponenteForm(BootstrapFormMixin, forms.Form):
    referencia = forms.CharField(max_length=50, label="Referencia del componente")
    nombre = forms.CharField(max_length=100, label="Nombre del componente")
    observacion_componente = forms.CharField(
        widget=forms.Textarea, required=False, label="Observación del retiro"
    )
    foto_frontal = forms.ImageField(label="Nueva foto frontal")
    foto_trasera = forms.ImageField(label="Nueva foto trasera")
    observacion_foto = forms.CharField(
        widget=forms.Textarea, required=False, label="Descripción de esta versión"
    )