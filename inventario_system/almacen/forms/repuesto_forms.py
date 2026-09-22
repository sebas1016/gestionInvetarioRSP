from django import forms
from ..models import Repuesto
from .mixins import BootstrapFormMixin

class RepuestoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ["modelo", "tipo", "referencia", "descripcion", "stock_minimo", "codigo_barras"]
        labels = {
            "codigo_barras": "Código de barras",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["referencia"].required = False
        self.fields["descripcion"].required = False
        self.fields["codigo_barras"].required = False
        self.fields["codigo_barras"].help_text = (
            "Déjalo vacío para que el sistema genere uno automáticamente."
        )

    def clean_referencia(self):
        # Guarda None en vez de "" para no chocar con la restricción unique
        # cuando se dejan varios repuestos sin referencia.
        return self.cleaned_data.get("referencia") or None

    def clean_codigo_barras(self):
        codigo = self.cleaned_data.get("codigo_barras")
        codigo = codigo.strip() if codigo else codigo
        return codigo or None