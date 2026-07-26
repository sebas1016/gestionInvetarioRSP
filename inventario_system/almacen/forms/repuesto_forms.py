from django import forms
from ..models import Repuesto
from .mixins import BootstrapFormMixin

class RepuestoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ["modelo", "tipo", "referencia", "descripcion", "stock_minimo"]