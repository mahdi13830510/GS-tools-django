from typing import Self
from uuid import UUID

from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, status

from gs_tools_django.files.models import File
from gs_tools_django.files.permissions import HasFileAccess
from gs_tools_django.files.serializers import FileSerializer, FileUploadSerializer
from gs_tools_django.files.services import FileService


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self: Self, request: Request):
        serializer = FileUploadSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        service = FileService(request.user)
        file = service.create_file_for_user(serializer.validated_data["file"])

        return Response(
            FileSerializer(file, context={"request": request}).data, status=status.HTTP_201_CREATED
        )


class FileSingleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser | HasFileAccess]
    parser_classes = [MultiPartParser, FormParser]

    def get(self: Self, request: Request, file_id: UUID):
        file = self.get_object(file_id)

        return Response(
            FileSerializer(file, context={"request": request}).data, status=status.HTTP_200_OK
        )

    def delete(self, request: Request, file_id: UUID):
        file = self.get_object(file_id)
        file.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self: Self, file_id: UUID):
        queryset = self.get_queryset()
        file = get_object_or_404(queryset, id=file_id)
        self.check_object_permissions(self.request, file)
        return file

    def get_queryset(self: Self):
        if self.request.user.is_superuser:
            return File.objects.all()
        return File.objects.filter(user=self.request.user)
