from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    """Validator for file size."""

    def __init__(self, max_size: int, min_size: int = 0):
        """Create a validator for file size.

        Args:
            max_size (int): max size in megabytes
            min_size (int): min size in megabytes
        """
        self.max_size = max_size * 1000000
        self.min_size = min_size * 1000000

    def __call__(self, file):
        if not self.min_size <= file.size <= self.max_size:
            message = _("File size must be between %(min_size)s and %(max_size)s")
            raise ValidationError(message % self.min_size % self.max_size)
