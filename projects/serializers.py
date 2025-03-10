from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from cloudinary.utils import cloudinary_url

from .models import Project
import os


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
        fields = ['title', 'prefix', 'suffix', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get("request")
        allowed_referrers = [os.getenv('FRONTEND_URL')]
        referer = request.META.get("HTTP_REFERER", "")

        if not settings.DEBUG:
            if not any(domain in referer for domain in allowed_referrers):
                return Response({"error": "Unauthorized"}, status=403)
            
            url, _ = cloudinary_url(
                obj.image.public_id,
                sign_url=True
            )
            return url
        return request.build_absolute_uri(obj.image.url) if obj.image else None