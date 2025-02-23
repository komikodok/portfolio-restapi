from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "phone_number", "message"]
        error_messages = {
            "first_name": {
                "required": "Please enter your first name.",
                "max_length": "Ensuring the first name has a maximum of 20 characters.",
            },
            "last_name": {
                "required": "Please enter your last name.",
                "max_length": "Ensuring the last name has a maximum of 20 characters.",
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
