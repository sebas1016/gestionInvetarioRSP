from django.db import models
from .unidad_repuesto import UnidadRepuesto


class ComponenteRetirado(models.Model):

    unidad=models.ForeignKey(
        UnidadRepuesto,
        on_delete=models.CASCADE,
        related_name='componentes'
    )

    referencia=models.CharField(
        max_length=50
    )

    nombre=models.CharField(
        max_length=100
    )

    observacion=models.TextField(
        blank=True
    )

    fecha=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.referencia} - {self.nombre}"