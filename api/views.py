from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ApiRootView(APIView):

    def get(self, request, *args, **kwargs):
        api_endpoints = {
            "contact": request.build_absolute_uri("contact"),
            "projects": request.build_absolute_uri("projects"),
            "assistant": request.build_absolute_uri("assistant"),
        }
        return Response(api_endpoints, status=status.HTTP_200_OK)