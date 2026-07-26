from django.db import models
from .marca import Marca
from .modelo import Modelo
from .tipo_repuesto import TipoRepuesto

class Repuesto(models.Model):

    #marca=models.ForeignKey(
     #   Marca,
      #  on_delete=models.PROTECT
    #)
    codigo=models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    modelo=models.ForeignKey(
        Modelo,
        on_delete=models.PROTECT
    )

    tipo=models.ForeignKey(
        TipoRepuesto,
        on_delete=models.PROTECT
    )

    referencia=models.CharField(
        max_length=100,
        unique=True
    )

    descripcion=models.TextField()
    
    stock_actual=models.PositiveIntegerField(
        default=0
    )

    stock_minimo=models.IntegerField(
        default=1
    )

    fecha_creacion=models.DateTimeField(
        auto_now_add=True
    )
    
    codigo_barras = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    imagen_codigo_barras = models.ImageField(
        upload_to='codigos_barras_repuesto/',
        blank=True,
        null=True
    )
    
    class Meta:

        constraints = [

            models.UniqueConstraint(

                fields=[
                    'modelo',
                    'tipo',
                    'referencia'
                ],

                name='uk_repuesto_modelo_tipo_referencia'
            )
        ]

    def __str__(self):
        return f"{self.modelo.marca.nombre} {self.modelo.nombre} - {self.tipo.nombre}"
    
    @property
    def stock(self):
        if self.tipo.es_serializado:
            return self.unidades.filter(
                estado__in=[
                    'NUEVA',
                    'FUNCIONAL'
                ]
            ).count()
        
        return self.stock_actual