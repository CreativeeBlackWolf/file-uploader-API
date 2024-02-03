from api.models import File
from django.forms.models import model_to_dict
from rest_framework import serializers


class FileUploadSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField(allow_empty_file=False))

    class Meta:
        model = File
        fields = ("id", "file", "files")
        read_only_fields = ("file",)

    def create(self, validated_data):
        files = validated_data.get("files")
        saved_files = []
        for file in files:
            f = File.objects.create(file=file)
            dict_model = model_to_dict(f)
            dict_model["file"] = dict_model["file"].path
            saved_files.append(dict_model)

        return {"files": [i for i in saved_files]}


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ("processed",)
