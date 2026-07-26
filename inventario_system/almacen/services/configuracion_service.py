from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError


class ConfiguracionService:

    @staticmethod
    def eliminar(instancia, mensaje_error):
        try:
            instancia.delete()
        except ProtectedError:
            raise ValidationError(mensaje_error)