from django.urls import path

from gs_tools_django.users.views import UserViewSet

app_name = "user"
urlpatterns = [
    path("", UserViewSet.as_view({"get": "list", "post": "create"}), name="list-create"),
    path("<uuid:pk>/", UserViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="retrieve-update"),
]