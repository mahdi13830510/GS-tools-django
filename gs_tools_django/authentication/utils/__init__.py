from gs_tools_django.settings import KAVENEGAR_API_KEY

from .kavenegar import KavenegarSMSProvider


def send_sms(phone_number, content):
    return KavenegarSMSProvider(KAVENEGAR_API_KEY).send_sms(
        phone_number,
        content,
    )
