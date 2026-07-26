from django.db import models
from .marca import Marca

class Modelo(models.Model):

    marca=models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='modelos'
    )

    nombre=models.CharField(
        max_length=100
    )
    
    def __str__(self):
        return f"{self.marca.nombre}-{self.nombre}"