from django.contrib import admin
from .models import Project, FrontendTest


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
    ]

admin.site.register(Project, ProjectAdmin)
