from django import forms
from django.forms import formset_factory

from ..models import Repuesto, Anaquel
from .mixins import BootstrapFormMixin


class RepuestoConTipoSelect(forms.Select):
    """
    Select de Repuesto que le agrega a cada <option> un atributo
    data-serializado ("true"/"false"), tomado de repuesto.tipo.es_serializado.

    Esto le permite al frontend mostrar automáticamente el formulario que
    corresponde (cantidad/anaquel para stock, o unidades con fotos para
    serializados) apenas se elige el repuesto, sin tener que preguntarle
    al usuario de antemano qué tipo de ingreso va a hacer.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializado_por_pk = {}

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value not in (None, ""):
            pk = value.value if hasattr(value, "value") else value
            es_serializado = self.serializado_por_pk.get(int(pk))
            if es_serializado is not None:
                option["attrs"]["data-serializado"] = "true" if es_serializado else "false"
        return option


class IngresoRepuestoForm(BootstrapFormMixin, forms.Form):
    """
    Único punto de entrada: se elige el repuesto (de cualquier tipo) y,
    según su tipo, la vista decide si se registra como stock o como
    unidades serializadas.
    """
    repuesto = forms.ModelChoiceField(
        queryset=Repuesto.objects.select_related("tipo", "modelo").order_by("modelo__nombre"),
        widget=RepuestoConTipoSelect(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["repuesto"].widget.serializado_por_pk = {
            repuesto.pk: repuesto.tipo.es_serializado
            for repuesto in self.fields["repuesto"].queryset
        }


class IngresoNoSerializadoDetalleForm(BootstrapFormMixin, forms.Form):
    """Datos adicionales para el ingreso de un repuesto por cantidad (stock)."""
    cantidad = forms.IntegerField(min_value=1)
    anaquel_destino = forms.ModelChoiceField(queryset=Anaquel.objects.all())
    observacion = forms.CharField(widget=forms.Textarea, required=False)


class UnidadIngresoForm(BootstrapFormMixin, forms.Form):
    anaquel = forms.ModelChoiceField(queryset=Anaquel.objects.all())
    foto_frontal = forms.ImageField()
    foto_trasera = forms.ImageField()
    observacion = forms.CharField(widget=forms.Textarea, required=False)


UnidadIngresoFormSet = formset_factory(UnidadIngresoForm, extra=1, can_delete=True)