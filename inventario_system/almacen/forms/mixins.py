from django import forms


class BootstrapFormMixin:
    """
    Agrega automáticamente las clases de Bootstrap 5 a los widgets de un form,
    para no repetir attrs={'class': ...} en cada campo de cada formulario.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            clase_existente = widget.attrs.get("class", "")

            if isinstance(widget, forms.CheckboxInput):
                nueva_clase = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                nueva_clase = "form-select"
            else:
                nueva_clase = "form-control"

            widget.attrs["class"] = f"{clase_existente} {nueva_clase}".strip()