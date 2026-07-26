from ..models import BoardRegistroFotografico


class FotoService:

    @staticmethod
    def crear_foto_inicial(unidad, frontal, trasera, descripcion=""):
        """
        Crea la primera versión del historial fotográfico de una unidad recién ingresada.
        El campo 'version' se calcula solo dentro del save() del modelo.
        """
        return BoardRegistroFotografico.objects.create(
            unidad=unidad,
            frontal=frontal,
            trasera=trasera,
            descripcion=descripcion,
        )
    
    @staticmethod
    def agregar_version_foto(unidad, frontal, trasera, descripcion=""):
        """
        Crea una nueva versión del historial fotográfico de la unidad.
        El campo 'version' se calcula solo (ver BoardRegistroFotografico.save()).
        Se usa tanto para la foto inicial del ingreso como para cada retiro posterior.
        """
        return BoardRegistroFotografico.objects.create(
            unidad=unidad,
            frontal=frontal,
            trasera=trasera,
            descripcion=descripcion,
        )