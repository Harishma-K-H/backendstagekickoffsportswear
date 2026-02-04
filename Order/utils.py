import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generate_upi_qr_code(upi_id, amount):
    upi_url = f"upi://pay?pa={upi_id}&pn=Merchant&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name="upi_qr.png")
