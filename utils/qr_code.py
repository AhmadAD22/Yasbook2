from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
import decimal
import qrcode

def generate_qr_code(data, service_order_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    return ContentFile(img_io.getvalue(), f'qr_code_{service_order_id}.png')