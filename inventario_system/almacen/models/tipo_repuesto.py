from django.db import models

class TipoRepuesto(models.Model):

    nombre=models.CharField(
        max_length=100
    )

    es_serializado=models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.nombre