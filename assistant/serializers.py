from rest_framework import serializers

from .models import Assistant
from django.conf import settings
from cloudinary.utils import cloudinary_url


class AssistantSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Assistant
        fields = ["mood", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        
        if not settings.DEBUG:
            url, _ = cloudinary_url(
                obj.image.public_id,
                sign_url=True
            )
            return url
        return request.build_absolute_uri(obj.image.url) if obj.image else None