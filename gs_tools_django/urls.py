"""
URL configuration for gs_tools_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include

from gs_tools_django import settings
from gs_tools_django.users.urls import urlpatterns as user_urls
from gs_tools_django.authentication.urls import urlpatterns as auth_urls

api_urlpatterns = [
    path("users/", include("gs_tools_django.users.urls")),
    path("auth/", include(auth_urls)),
]

urlpatterns = [
    path("api/v1/", include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # django-debug-toolbar
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]