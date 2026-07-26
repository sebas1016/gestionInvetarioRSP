"""from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models.unidad_repuesto import UnidadRepuesto
from .services.codigo_service import CodigoService
from .services.qr_service import QRService
from .services.inventario_service import (
    InventarioService
)

@receiver(
    pre_save,
    sender=UnidadRepuesto
)
def generar_codigo_qr(
    sender,
    instance,
    **kwargs
):

    if not instance.codigo_unico:

        codigo=CodigoService.generar_codigo(
            instance.repuesto.tipo
        )

        instance.codigo_unico=codigo
        instance.codigo_barras=codigo

        QRService.generar_qr(
            instance,
            codigo
        )

@receiver(
    post_save,
    sender=UnidadRepuesto
)
def crear_entrada(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        InventarioService.entrada(

            repuesto=instance.repuesto,

            cantidad=1
        )"""