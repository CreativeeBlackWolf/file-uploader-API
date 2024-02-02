from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from api.models import File
from api.serializers import FileSerializer
from api.tasks import handle_file

import celery


class FileAPIViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class UploadFileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save()
                    # celery.current_app.send_task("app.tasks.handle_file", (id,))
                    handle_file.delay(serializer.data["id"])
                    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(
                        {"error": "probably file was not uploaded"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as e:
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
