from rest_framework import serializers

from .models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ("uploaded_at", "processed",)

class FileOutSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(source="file.name")
    file_url = serializers.CharField(source="file.url")

    class Meta:
        model = File
        fields = ("id","filename", "file_url", "uploaded_at", "processed",)
        read_only_fields = fields
