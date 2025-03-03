from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from .forms import ContactForm
from .serializers import ContactSerializer
from mysite.settings import EMAIL_HOST_USER
from log import logger

class ContactAPIView(APIView):

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.data or None)
        if form.is_valid():
            contact = form.save()
            data = ContactSerializer(contact).data

            message = f"""
                You received a new contact message.

                Name: {data['first_name']} {data['last_name']}
                Email: {data['email']}
                Message : {data['message']}
            """

            try:
                send_mail(
                    f"New message from {data['email']}",
                    message=message,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=["adm.fazport@gmail.com"],
                    fail_silently=False
                )
            except Exception as error:
                logger.error(f"Error: {error}")
                return Response({
                    "status": "error",
                    "message": "contact message is created but failed to sended message.",
                    "error": str(error)
                })

            return Response({
                "status": "ok",
                "message": "contact message is created successfully and email sended to admin."
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "errors",
            "message": "Failed to create contact message!",
            "errors": form.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
