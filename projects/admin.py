from django.contrib import admin

from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

admin.site.register(Project, ProjectAdmin)