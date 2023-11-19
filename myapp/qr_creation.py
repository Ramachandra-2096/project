import secrets
import qrcode
from .models import Event,PurchasedTicket
from qrcode.image.pil import PilImage
import os

def generate_qr_code(user,event):
    new_token = secrets.token_urlsafe(200)

    # Ensure the generated token is unique for the user profile
    while PurchasedTicket.objects.filter(id=user.id, token=new_token).exists():
        new_token = secrets.token_urlsafe(200)
    ticket, created = PurchasedTicket.objects.get_or_create(user=user, event=event)
    ticket.token = new_token
    ticket.save()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(new_token)
    qr.make(fit=True)
    # Use a specific class from qrcode.image module
    img = qr.make_image(fill_color="black", back_color="white", image_factory=PilImage)
    save_path = os.path.join('static',user.first_name+".jpg")
    img.save(save_path)

    return save_path
  