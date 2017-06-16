from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, FrontendTest, Report, LotrekUser, Machine, Reseller


class LotrekUserAdmin(UserAdmin):
    fieldsets = ()
    exclude = ('groups',)
    readonly_fields = ('last_login', 'date_joined',)


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest
    extra = 1


class ResellerAdmin(admin.ModelAdmin):
    pass


class MachineAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {'fields': ('name', 'reseller', 'end_time')}),
        (_('Ssh'), {'fields': ('server_address', 'ssh_username', 'ssh_password')}),
    )
    list_display = ('name', 'server_address', 'reseller', 'end_time')


class ReportInline(admin.TabularInline):
    model = Report
    extra = 1

    readonly_fields = ('project', 'date', 'text', 'class_type',)


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
        ReportInline,
    ]
    fieldsets = (
        (_('General'), {'fields': ('name', 'slug', 'live_url', 'team', 'machine')}),
        (_('Backup'), {'fields': ('backup_active', 'backup_archive', 'backup_script', 'backup_sync_folders')}),
    )
    readonly_fields = ('slug',)
    filter_horizontal = ('team',)
    list_display = ('name', 'live_url', 'backup_active', 'machine')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'class_type')
    readonly_fields = ('project', 'date', 'text', 'class_type')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LotrekUser, LotrekUserAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Reseller, ResellerAdmin)

