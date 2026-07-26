from django.db import models
from ..models import Repuesto
from ..models import Anaquel


class UnidadRepuesto(models.Model):

    ESTADOS = [

        ('NUEVA','Nueva'),
        ('FUNCIONAL','Funcional'),
        ('USADA','Usada'),
        ('DESARMADA','Desarmada'),
        ('DEFECTUOSA','Defectuosa')

    ]

    repuesto=models.ForeignKey(
        Repuesto,
        on_delete=models.CASCADE,
        related_name='unidades'
    )

    codigo_unico=models.CharField(
    max_length=100,
    unique=True,
    blank=True,
    null=True
)

    codigo_barras=models.CharField(
    max_length=100,
    unique=True,
    blank=True,
    null=True
    )

    imagen_codigo_barras = models.ImageField(
        upload_to='codigos_barras/',
        blank=True,
        null=True
    )

    anaquel=models.ForeignKey(
        Anaquel,
        on_delete=models.PROTECT
    )

    estado=models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='NUEVA'
    )

    fecha_ingreso=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.codigo_unico