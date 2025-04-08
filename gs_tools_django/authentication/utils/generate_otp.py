import secrets

from gs_tools_django.settings import OTP_LENGTH

def generate_otp_code():
    digits = []

    for _ in range(OTP_LENGTH):
        digits.append(str(secrets.randbelow(10)))

    return "".join(digits)