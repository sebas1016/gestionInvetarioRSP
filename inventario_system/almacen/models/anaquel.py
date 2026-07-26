from django.db import models

class Anaquel(models.Model):

    codigo=models.CharField(
        max_length=50,
        unique=True
    )

    descripcion=models.TextField(
        blank=True
    )

    def __str__(self):
        return self.codigo