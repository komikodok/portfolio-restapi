from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Assistant(models.Model):
    choice = (
        ("normal", "normal"),
        ("happy", "happy"),
        ("sad", "sad")
    )
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