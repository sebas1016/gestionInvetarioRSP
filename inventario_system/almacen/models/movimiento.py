from django.db import models
from django.contrib.auth.models import User

from almacen.models import Repuesto
from .unidad_repuesto import UnidadRepuesto
from .anaquel import Anaquel


class MovimientoInventario(models.Model):

    TIPOS=[

        ('ENTRADA','Entrada'),
        ('SALIDA','Salida'),
        ('TRASLADO', 'Traslado')
    ]

    repuesto=models.ForeignKey(
        Repuesto,
        on_delete=models.CASCADE
    )

    unidad=models.ForeignKey(
        UnidadRepuesto,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    tipo=models.CharField(
        max_length=20,
        choices=TIPOS
    )
    
    anaquel_origen=models.ForeignKey(
        Anaquel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimientos_salida'
    )

    anaquel_destino=models.ForeignKey(
        Anaquel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimientos_entrada'
    )
    
    cantidad=models.PositiveIntegerField()

    usuario=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    observacion=models.TextField(
        blank=True
    )

    fecha=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.tipo} {self.repuesto}"