from api.views import FileAPIViewSet, UploadFileAPIView
from django.urls import include, path
from rest_framework import routers

app_name = "api"

router = routers.SimpleRouter()
router.register("files", FileAPIViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("upload/", UploadFileAPIView.as_view()),
]
