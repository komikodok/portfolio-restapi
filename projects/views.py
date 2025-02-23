from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer

class ProjectListView(ListAPIView):
    queryset = Project.objects.order_by("-view_count").all()
    serializer_class = ProjectListSerializer

class ProjectDetailView(RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    lookup_field = "slug"

    def get_object(self):
        obj = get_object_or_404(Project, slug=self.kwargs.get(self.lookup_field))
        obj.view_count += 1
        obj.save()
        return obj
