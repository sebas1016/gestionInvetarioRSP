from django.db import transaction
from ..models import Correlativo


class CodigoService:

    PREFIJO_UNIDAD = "UN"

    @staticmethod
    @transaction.atomic
    def generar_codigo_unico(prefijo):
        correlativo, _ = Correlativo.objects.select_for_update().get_or_create(
            prefijo=prefijo,
            defaults={"ultimo_numero": 0},
        )
        correlativo.ultimo_numero += 1
        correlativo.save(update_fields=["ultimo_numero"])
        return f"{prefijo}-{correlativo.ultimo_numero:06d}"