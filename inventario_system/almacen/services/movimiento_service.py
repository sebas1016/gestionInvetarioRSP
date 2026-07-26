from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Q
from ..models import Repuesto, MovimientoInventario


class MovimientoService:

    @staticmethod
    @transaction.atomic
    def registrar_salida_no_serializado(repuesto, cantidad, anaquel_origen, usuario, observacion=""):
        repuesto = Repuesto.objects.select_for_update().get(pk=repuesto.pk)

        if cantidad > repuesto.stock_actual:
            raise ValidationError(
                f"No hay stock suficiente. Disponible: {repuesto.stock_actual}, solicitado: {cantidad}."
            )

        repuesto.stock_actual -= cantidad
        repuesto.save(update_fields=["stock_actual"])

        return MovimientoInventario.objects.create(
            repuesto=repuesto,
            unidad=None,
            tipo="SALIDA",
            anaquel_origen=anaquel_origen,
            cantidad=cantidad,
            usuario=usuario,
            observacion=observacion,
        )

    @staticmethod
    @transaction.atomic
    def registrar_salida_serializada(unidad, nuevo_estado, usuario, observacion=""):
        unidad.estado = nuevo_estado
        unidad.save(update_fields=["estado"])

        return MovimientoInventario.objects.create(
            repuesto=unidad.repuesto,
            unidad=unidad,
            tipo="SALIDA",
            anaquel_origen=unidad.anaquel,
            cantidad=1,
            usuario=usuario,
            observacion=observacion,
        )
        
    @staticmethod
    def listar_movimientos(tipo=None, busqueda="", fecha_desde=None, fecha_hasta=None):
        qs = (
            MovimientoInventario.objects
            .select_related("repuesto", "unidad", "anaquel_origen", "anaquel_destino", "usuario")
            .order_by("-fecha")
        )

        if tipo:
            qs = qs.filter(tipo=tipo)

        if busqueda:
            qs = qs.filter(
                Q(repuesto__referencia__icontains=busqueda) |
                Q(unidad__codigo_unico__icontains=busqueda)
            )

        if fecha_desde:
            qs = qs.filter(fecha__date__gte=fecha_desde)

        if fecha_hasta:
            qs = qs.filter(fecha__date__lte=fecha_hasta)

        return qs