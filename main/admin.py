from django.contrib import admin
from .models import Project, FrontendTest, Report, LotrekUser

from django.utils.translation import gettext_lazy as _


class LotrekUserAdmin(admin.ModelAdmin):
    model = LotrekUser


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
    ]
    fieldsets = (
        (_('General'), {'fields': ('name', 'slug', 'live_url', 'team')}),
        (_('Ssh'), {'fields': ('server_address', 'ssh_username', 'ssh_password')}),
        (_('Backup'), {'fields': ('backup_archive', 'backup_script', 'backup_active')}),
    )
    readonly_fields = ('slug',)
    filter_horizontal = ('team',)
    list_display = ('name', 'live_url', 'backup_active')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'class_type')
    readonly_fields = ('project', 'date', 'text', 'class_type')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LotrekUser, LotrekUserAdmin)
