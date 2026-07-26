from ..models import Repuesto, UnidadRepuesto, MovimientoInventario, Anaquel


class DashboardService:

    @staticmethod
    def obtener_resumen():
        return {
            "total_repuestos": Repuesto.objects.count(),
            "total_unidades": UnidadRepuesto.objects.count(),
            "total_movimientos": MovimientoInventario.objects.count(),
            "total_anaqueles": Anaquel.objects.count(),
        }