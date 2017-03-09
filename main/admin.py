from django.contrib import admin
from .models import Project, FrontendTest, Report


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
    ]


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
