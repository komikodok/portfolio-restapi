from django.db import models
from django.contrib.auth import get_user_model


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
    mood = models.CharField(max_length=10, choices=choice)
    image = models.ImageField(upload_to="assistant/")

    def __str__(self) -> str:
        return self.mood