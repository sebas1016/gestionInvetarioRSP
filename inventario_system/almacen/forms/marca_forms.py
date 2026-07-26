from django import forms
from almacen.models import Marca


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = ["nombre"]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la marca"
                }
            )
        }