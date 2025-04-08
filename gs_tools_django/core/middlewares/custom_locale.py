from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate

class CustomLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language_code = request.META.get("HTTP_X_ACCEPT_LANGUAGE")
        if not language_code:
            language_code = settings.LANGUAGE_CODE
        activate(language_code)
        request.LANGUAGE_CODE = language_code