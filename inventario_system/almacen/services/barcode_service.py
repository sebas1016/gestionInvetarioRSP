import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile


class BarcodeService:

    @staticmethod
    def generar_codigo_barras(objeto, campo_codigo, campo_imagen):
        """
        Genera una imagen Code128 a partir de getattr(objeto, campo_codigo)
        y la guarda en getattr(objeto, campo_imagen). Sirve para cualquier
        modelo que tenga un campo de texto único y un ImageField.
        """
        valor_codigo = getattr(objeto, campo_codigo)

        code128 = barcode.get_barcode_class("code128")
        instancia = code128(valor_codigo, writer=ImageWriter())

        buffer = BytesIO()
        instancia.write(buffer)
        nombre_archivo = f"{valor_codigo}.png"

        campo_imagen_obj = getattr(objeto, campo_imagen)
        campo_imagen_obj.save(nombre_archivo, ContentFile(buffer.getvalue()), save=True)