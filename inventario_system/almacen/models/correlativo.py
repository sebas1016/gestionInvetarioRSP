from django.db import models


class Correlativo(models.Model):
    """
    Contador secuencial global para generar codigo_unico de UnidadRepuesto.
    Una sola fila por prefijo (ej: 'UN'). Race-safe vía select_for_update().
    """

    prefijo = models.CharField(max_length=10, unique=True)
    ultimo_numero = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prefijo} -> {self.ultimo_numero}"