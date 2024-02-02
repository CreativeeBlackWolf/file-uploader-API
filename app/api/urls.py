from django.urls import path, include
from rest_framework import routers
from api.views import FileAPIViewSet, UploadFileAPIView


app_name = "api"

router = routers.SimpleRouter()
router.register("files", FileAPIViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("upload/", UploadFileAPIView.as_view()),
]
