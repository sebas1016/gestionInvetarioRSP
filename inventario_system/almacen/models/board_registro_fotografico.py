from django.db import models
from .unidad_repuesto import UnidadRepuesto


class BoardRegistroFotografico(models.Model):

    unidad=models.ForeignKey(
        UnidadRepuesto,
        on_delete=models.CASCADE,
        related_name='fotos'
    )

    version=models.PositiveIntegerField(
        editable=False,
    )

    frontal=models.ImageField(
        upload_to='boards/frontal/'
    )

    trasera=models.ImageField(
        upload_to='boards/trasera/'
    )

    descripcion=models.TextField(
        blank=True
    )

    fecha=models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering=['-version']

        unique_together=[
            'unidad',
            'version'
        ]

    def __str__(self):

        return f"{self.unidad.codigo_unico} V{self.version}"
    
    def save(self,*args,**kwargs):

        if not self.pk:

            ultima=BoardRegistroFotografico.objects.filter(
                unidad=self.unidad
            ).order_by(
                '-version'
            ).first()

            self.version=1

            if ultima:

                self.version=ultima.version+1

        super().save(
            *args,
            **kwargs
        )