from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer

class ProjectListView(ListAPIView):
    queryset = Project.objects.order_by("-view_count").all()
    serializer_class = ProjectListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "ok",
            "data": serializer.data
        })


class ProjectDetailView(RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    lookup_field = "slug"

    def get_object(self):
        obj = get_object_or_404(Project, slug=self.kwargs.get(self.lookup_field))
        obj.view_count += 1
        obj.save()
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "ok",
            "data": serializer.data
        })
