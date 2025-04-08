from .generate_otp import generate_otp_code
from .kavenegar import KavenegarSMSProvider
from ...settings import KAVENEGAR_API_KEY


def send_sms(phone_number, content):
    return KavenegarSMSProvider(KAVENEGAR_API_KEY).send_sms(
        phone_number,
        content,
    )