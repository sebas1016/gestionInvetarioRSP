from django.db import transaction
from django.db.models import Q, OuterRef, Subquery
from ..models import Repuesto, UnidadRepuesto, MovimientoInventario, ComponenteRetirado
from .codigo_service import CodigoService
from .barcode_service import BarcodeService
from .foto_service import FotoService
from django.core.exceptions import ValidationError


class InventarioService:

    @staticmethod
    @transaction.atomic
    def eliminar_repuesto(repuesto):
        """
        Elimina un repuesto de forma DEFINITIVA e IRREVERSIBLE, exista o no
        stock, unidades o historial de movimientos asociado.

        Junto con el repuesto se eliminan en cascada (a nivel de base de
        datos): sus movimientos de inventario, sus unidades (si es
        serializado) y, de esas unidades, sus fotos y componentes retirados.
        Además, se borran del almacenamiento todas las imágenes relacionadas
        (código de barras del repuesto, de cada unidad, y las fotos
        frontal/trasera de cada unidad), para no dejar archivos huérfanos.
        """
        archivos_a_borrar = []

        if repuesto.imagen_codigo_barras:
            archivos_a_borrar.append(repuesto.imagen_codigo_barras)

        for unidad in repuesto.unidades.all():
            if unidad.imagen_codigo_barras:
                archivos_a_borrar.append(unidad.imagen_codigo_barras)
            for foto in unidad.fotos.all():
                if foto.frontal:
                    archivos_a_borrar.append(foto.frontal)
                if foto.trasera:
                    archivos_a_borrar.append(foto.trasera)

        repuesto.delete()

        for archivo in archivos_a_borrar:
            archivo.storage.delete(archivo.name)
        
  
    @staticmethod
    @transaction.atomic
    def registrar_ingreso_no_serializado(repuesto, cantidad, anaquel_destino, usuario, observacion=""):
        repuesto = Repuesto.objects.select_for_update().get(pk=repuesto.pk)
        repuesto.stock_actual += cantidad
        repuesto.save(update_fields=["stock_actual"])

        return MovimientoInventario.objects.create(
            repuesto=repuesto,
            unidad=None,
            tipo="ENTRADA",
            anaquel_destino=anaquel_destino,
            cantidad=cantidad,
            usuario=usuario,
            observacion=observacion,
        )
    """
    @staticmethod
    @transaction.atomic
    def registrar_ingreso_serializado(repuesto, unidades_data, usuario):
       
        unidades_creadas = []

        for data in unidades_data:
            codigo_unico = CodigoService.generar_codigo_unico()

            unidad = UnidadRepuesto.objects.create(
                repuesto=repuesto,
                codigo_unico=codigo_unico,
                codigo_barras=codigo_unico,
                anaquel=data["anaquel"],
                estado="NUEVA",
            )

            BarcodeService.generar_codigo_barras(unidad)

            FotoService.agregar_version_foto(
                unidad=unidad,
                frontal=data["foto_frontal"],
                trasera=data["foto_trasera"],
                descripcion=data.get("observacion", ""),
            )

            MovimientoInventario.objects.create(
                repuesto=repuesto,
                unidad=unidad,
                tipo="ENTRADA",
                anaquel_destino=data["anaquel"],
                cantidad=1,
                usuario=usuario,
                observacion=data.get("observacion", ""),
            )

            unidades_creadas.append(unidad)

        return unidades_creadas
    """
    @staticmethod
    def listar_repuestos(marca_id=None, tipo_id=None, busqueda=""):
        ultimo_anaquel = (
            MovimientoInventario.objects
            .filter(repuesto=OuterRef("pk"), anaquel_destino__isnull=False)
            .order_by("-fecha")
            .values("anaquel_destino__codigo")[:1]
        )

        qs = (
            Repuesto.objects
            .select_related("modelo__marca", "tipo")
            .annotate(anaquel_actual=Subquery(ultimo_anaquel))
            .order_by("modelo__marca__nombre", "modelo__nombre", "referencia")
        )

        if marca_id:
            qs = qs.filter(modelo__marca_id=marca_id)
        if tipo_id:
            qs = qs.filter(tipo_id=tipo_id)
        if busqueda:
            qs = qs.filter(
                Q(referencia__icontains=busqueda) | Q(descripcion__icontains=busqueda)
            )
        return qs

    @staticmethod
    def listar_unidades_de_repuesto(repuesto):
        return repuesto.unidades.select_related("anaquel").order_by("-fecha_ingreso")

    @staticmethod
    def listar_movimientos_de_repuesto(repuesto, limite=20):
        return (
            MovimientoInventario.objects
            .filter(repuesto=repuesto)
            .select_related("anaquel_origen", "anaquel_destino", "usuario")
            .order_by("-fecha")[:limite]
        )
    
    @staticmethod
    @transaction.atomic
    def registrar_retiro_componente(unidad, data, usuario):
        ComponenteRetirado.objects.create(
            unidad=unidad,
            referencia=data["referencia"],
            nombre=data["nombre"],
            observacion=data.get("observacion_componente", ""),
        )

        FotoService.agregar_version_foto(
            unidad=unidad,
            frontal=data["foto_frontal"],
            trasera=data["foto_trasera"],
            descripcion=data.get("observacion_foto", ""),
        )

        unidad.estado = "DESARMADA"
        unidad.save(update_fields=["estado"])

        MovimientoInventario.objects.create(
            repuesto=unidad.repuesto,
            unidad=unidad,
            tipo="SALIDA",
            anaquel_origen=unidad.anaquel,
            cantidad=1,
            usuario=usuario,
            observacion=f"Retiro de componente: {data['nombre']} ({data['referencia']})",
        )

        return unidad
    
#Busqueda barcode

    @staticmethod
    @transaction.atomic
    def registrar_ingreso_serializado(repuesto, unidades_data, usuario):
        unidades_creadas = []

        for data in unidades_data:
            codigo = CodigoService.generar_codigo_unico("UN")

            unidad = UnidadRepuesto.objects.create(
                repuesto=repuesto,
                codigo_unico=codigo,
                codigo_barras=codigo,
                anaquel=data["anaquel"],
                estado="NUEVA",
            )

            BarcodeService.generar_codigo_barras(unidad, "codigo_barras", "imagen_codigo_barras")

            FotoService.agregar_version_foto(
                unidad=unidad,
                frontal=data["foto_frontal"],
                trasera=data["foto_trasera"],
                descripcion=data.get("observacion", ""),
            )

            MovimientoInventario.objects.create(
                repuesto=repuesto,
                unidad=unidad,
                tipo="ENTRADA",
                anaquel_destino=data["anaquel"],
                cantidad=1,
                usuario=usuario,
                observacion=data.get("observacion", ""),
            )

            unidades_creadas.append(unidad)

        return unidades_creadas

    @staticmethod
    @transaction.atomic
    def crear_repuesto(datos_validados):
        datos_validados = dict(datos_validados)
        codigo_manual = datos_validados.pop("codigo_barras", None)

        repuesto = Repuesto.objects.create(**datos_validados)

        repuesto.codigo_barras = codigo_manual or CodigoService.generar_codigo_unico("RP")
        repuesto.save(update_fields=["codigo_barras"])

        BarcodeService.generar_codigo_barras(repuesto, "codigo_barras", "imagen_codigo_barras")
        return repuesto

    @staticmethod
    @transaction.atomic
    def actualizar_repuesto(repuesto, datos_validados, codigo_anterior):
        for campo, valor in datos_validados.items():
            if campo == "codigo_barras":
                continue
            setattr(repuesto, campo, valor)

        repuesto.codigo_barras = datos_validados.get("codigo_barras") or CodigoService.generar_codigo_unico("RP")
        repuesto.save()

        if repuesto.codigo_barras != codigo_anterior:
            BarcodeService.generar_codigo_barras(repuesto, "codigo_barras", "imagen_codigo_barras")

        return repuesto
    
    @staticmethod
    def obtener_anaquel_sugerido(repuesto):
        """
        Devuelve el último anaquel_destino usado en un movimiento de ENTRADA
        para este repuesto, como sugerencia de "dónde está" normalmente.
        None si el repuesto nunca ha tenido un ingreso registrado.
        """
        ultimo_movimiento = (
            MovimientoInventario.objects
            .filter(repuesto=repuesto, anaquel_destino__isnull=False)
            .order_by("-fecha")
            .first()
        )
        return ultimo_movimiento.anaquel_destino if ultimo_movimiento else None
    
    @staticmethod
    def buscar_por_codigo(codigo):
        """
        Devuelve una tupla (tipo, objeto) donde tipo es 'unidad' o 'repuesto',
        o (None, None) si no se encuentra nada.
        """
        unidad = UnidadRepuesto.objects.filter(codigo_barras=codigo).first()
        if unidad:
            return "unidad", unidad

        repuesto = Repuesto.objects.filter(codigo_barras=codigo).first()
        if repuesto:
            return "repuesto", repuesto

        return None, None
    
    