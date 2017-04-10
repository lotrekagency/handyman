from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, FrontendTest, Report, LotrekUser


class LotrekUserAdmin(UserAdmin):
    fieldsets = ()
    exclude = ('groups',)
    readonly_fields = ('last_login', 'date_joined',)


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
        (_('Backup'), {'fields': ('backup_active', 'backup_archive', 'backup_script', 'backup_sync_folders')}),
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
