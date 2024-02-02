from rest_framework import serializers
from .models import File


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ("processed",)
