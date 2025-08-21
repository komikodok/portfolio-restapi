from django.conf import settings
from rest_framework import serializers
from cloudinary.utils import cloudinary_url

from .models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'slug', 'github', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url) if obj.image else None
    
class ProjectDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'body', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get("request")

        if not settings.DEBUG:
            url, _ = cloudinary_url(
                obj.image.public_id,
                sign_url=True
            )
            return url
        return request.build_absolute_uri(obj.image.url) if obj.image else None