import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


class QRService:

    @staticmethod
    def generar_qr(instancia, codigo):

        qr = qrcode.make(codigo)

        buffer = BytesIO()

        qr.save(buffer, format='PNG')

        nombre_archivo = f"{codigo}.png"

        instancia.qr.save(
            nombre_archivo,
            ContentFile(buffer.getvalue()),
            save=False
        )