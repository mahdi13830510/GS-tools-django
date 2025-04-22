from django.urls import path

from gs_tools_django.files.views import FileSingleView, FileUploadView

urlpatterns = [
    path("upload/", view=FileUploadView.as_view()),
    path("<uuid:file_id>/", view=FileSingleView.as_view()),
]
