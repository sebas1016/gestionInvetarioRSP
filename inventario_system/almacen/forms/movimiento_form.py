from django import forms
from ..models.movimiento import MovimientoInventario
from ..models.anaquel import Anaquel
from .mixins import BootstrapFormMixin


class MovimientoForm(BootstrapFormMixin, forms.ModelForm):
    anaquel=forms.ModelChoiceField(
        queryset=Anaquel.objects.all(),
        required=False
    )

    class Meta:

        model=MovimientoInventario

        fields=[

            'repuesto',
            'unidad',
            'tipo',
            'cantidad',
            'anaquel',
            'observacion'

        ]
        
#Salidas
from django import forms
from ..models import Anaquel, UnidadRepuesto


class SalidaNoSerializadoForm(BootstrapFormMixin, forms.Form):
    cantidad = forms.IntegerField(min_value=1)
    anaquel_origen = forms.ModelChoiceField(queryset=Anaquel.objects.all())
    observacion = forms.CharField(widget=forms.Textarea, required=False)


class SalidaSerializadoForm(BootstrapFormMixin, forms.Form):
    nuevo_estado = forms.ChoiceField(choices=UnidadRepuesto.ESTADOS)
    observacion = forms.CharField(widget=forms.Textarea, required=False)