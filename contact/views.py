from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import ContactForm

class ContactAPIView(APIView):

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.data or None)
        if form.is_valid():
            form.save()
            return Response({
                "status": "ok",
                "message": "contact message is created successfully."
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "errors",
            "message": "Failed to create contact message!",
            "errors": form.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
