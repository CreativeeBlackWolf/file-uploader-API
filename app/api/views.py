from api.models import File
from api.serializers import FileSerializer, FileUploadSerializer
from django.db import transaction
from django.http import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


class FileAPIViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class UploadFileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        serializer.instance, status=status.HTTP_201_CREATED
                    )
                else:
                    return JsonResponse(
                        {
                            "files": "This field is required or files we're not uploaded via form-body"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as e:
            print(str(e))
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def page_not_found_view(request, exception):
    return JsonResponse(
        {
            "error": "You got 404'd. Proceed to /api/files/ if you want to see all uploaded files. Proceed to /api/upload/ to upload a file."
        },
        status=status.HTTP_404_NOT_FOUND,
    )
