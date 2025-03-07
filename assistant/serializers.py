from rest_framework import serializers

from .models import Assistant
from django.conf import settings

# class MessageHistorySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = MessageHistory
#         fields = ['user', 'message', 'timestamp']


class AssistantSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Assistant
        fields = ["mood", "image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url) if obj.image else None