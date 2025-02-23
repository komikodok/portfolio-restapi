from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name}"
