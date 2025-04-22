from django.urls import path

from gs_tools_django.profiles.views import ProfileViewSet

app_name = "profiles"

urlpatterns = [
    path("", ProfileViewSet.as_view({"get": "list", "post": "create"}), name="list"),
    path(
        "<uuid:pk>/",
        ProfileViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="retrieve",
    ),
]
