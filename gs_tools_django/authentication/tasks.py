from celery import shared_task
from phonenumber_field.phonenumber import to_python as parse_phone
from gs_tools_django.authentication.utils import send_sms

@shared_task
def send_otp_sms(phone_number: str, code):
    phone_number = parse_phone(phone_number).as_e164
    response = send_sms(phone_number, code)
    print(response)