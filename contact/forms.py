from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone_number", "message"]
        error_messages = {
            "name": {
                "required": "Please enter your name.",
                "max_length": "Ensuring the first name has a maximum of 20 characters.",
            },
            "email": {
                "required": "We need your email address to contact you.",
                "invalid": "Please enter a valid email address.",
            },
            "phone_number": {
                "max_length": "Ensuring the phone number has a maximum of 15 characters.",
            },
            "message": {
                "required": "Please include a message.",
            },
        }
