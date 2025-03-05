from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
import cloudinary
from cloudinary.models import CloudinaryField
import os


class MessageHistory(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="messages_history", on_delete=models.CASCADE, null=True)
    message = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        username = "AnonymousUser" if self.user is None else self.user.get_username()
        message = self.message[-1].get("content", "")
        return f"{username}: {message}"
    

class Assistant(models.Model):
    choice = (
        ("normal", "normal"),
        ("happy", "happy"),
        ("sad", "sad")
    )
    public_id = models.CharField(max_length=255, blank=True, null=True)
    mood = models.CharField(max_length=10, choices=choice)
    if settings.DEBUG:
        image = models.ImageField(upload_to="assistant/")
    else:
        image = CloudinaryField(
            "image", 
            folder="assistant/", 
            resource_type="image",
            type="authenticated"
        )

    def __str__(self) -> str:
        return self.mood