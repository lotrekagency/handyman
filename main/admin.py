from django.contrib import admin
from .models import Project, FrontendTest, Report, LotrekUser


class LotrekUserAdmin(admin.ModelAdmin):
    model = LotrekUser


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
    ]
    filter_horizontal = ('team',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LotrekUser, LotrekUserAdmin)
