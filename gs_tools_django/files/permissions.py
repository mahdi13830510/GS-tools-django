from typing import Self

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from gs_tools_django.files.models import File, UserFile


class HasFileAccess(BasePermission):
    def has_object_permission(self: Self, request: Request, view: APIView, file: File):
        return file.created_by == request.user or UserFile.objects.filter(
            user=request.user, file=file
        )
