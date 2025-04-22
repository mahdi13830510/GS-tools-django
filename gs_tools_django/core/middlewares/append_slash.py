from django.utils.deprecation import MiddlewareMixin


class AppendSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the URL does not have a trailing slash and does not have a file extension
        if not request.path.endswith("/") and "." not in request.path:
            # Rewrite the URL by adding a trailing slash
            request.path_info = request.path + "/"
