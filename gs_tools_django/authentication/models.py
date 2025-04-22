from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from gs_tools_django.authentication.managers import SMSLoginRequestManager
from gs_tools_django.authentication.tasks import send_otp_sms
from gs_tools_django.authentication.utils.generate_otp import generate_otp_code
from gs_tools_django.core.models import TimeStampedModel, UUIDModel


class SMSLoginRequest(UUIDModel, TimeStampedModel):
    phone_number = PhoneNumberField(_("Phone number"), null=False)

    code = models.CharField(
        _("Code"),
        null=False,
        blank=False,
        max_length=6,
        default=generate_otp_code,
    )
    expires_at = models.DateTimeField(_("Expires at"), null=False)
    is_sent = models.BooleanField(_("Is sent"), null=False, default=False)

    objects = SMSLoginRequestManager()

    class Meta:
        verbose_name = _("SMS login request")
        verbose_name_plural = _("SMS login requests")

    def save(self, *args, **kwargs) -> None:
        if self.expires_at is None:
            self.expires_at = timezone.now() + settings.OTP_LIFETIME_SECONDS

        return super().save(*args, **kwargs)

    def send(self) -> None:
        send_otp_sms.delay(self.phone_number.as_e164, self.code)
        self.is_sent = True
