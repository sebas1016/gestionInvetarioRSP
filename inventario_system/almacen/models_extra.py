from django.db import models


class Marca(models.Model):
    nombre=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nombre 


class Modelo(models.Model):

    marca=models.ForeignKey(
        Marca,
        on_delete=models.CASCADE
    )

    nombre=models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.marca}-{self.nombre}"


class TipoRepuesto(models.Model):

    nombre=models.CharField(
        max_length=100
    )

    es_serializado=models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.nombre


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


class Repuesto(models.Model):

    marca=models.ForeignKey(
        Marca,
        on_delete=models.PROTECT
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

    stock_minimo=models.IntegerField(
        default=1
    )

    fecha_creacion=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.tipo} {self.modelo}"