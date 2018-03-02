from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, FrontendTest, Report, LotrekUser, Machine, Reseller, Deadline, Domain, Registar


class LotrekUserAdmin(UserAdmin):
    actions = []
    fieldsets = ()
    exclude = ('groups',)
    readonly_fields = ('last_login', 'date_joined',)


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest
    extra = 1


class ResellerAdmin(admin.ModelAdmin):
    pass


class DeadlineInline(admin.TabularInline):
    model = Deadline
    extra = 1


class MachineAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {'fields': ('name', 'name_on_reseller', 'end_time')}),
        (_('Reseller'), {'fields': ('reseller', 'reseller_panel', 'reseller_panel_username', 'reseller_panel_password')}),
        (_('Ssh'), {'fields': ('server_address', 'ssh_username', 'ssh_password')}),
        (_('Online panel'), {'fields': ('online_panel', 'online_panel_username', 'online_panel_password')}),
    )
    list_display = ('name', 'server_address', 'reseller', 'end_time')


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
        DeadlineInline
    ]
    fieldsets = (
        (_('General'), {'fields': ('name', 'slug', 'live_url', 'team', 'machine')}),
        (_('Backup'), {'fields': ('backup_active', 'backup_archive', 'backup_script', 'backup_sync_folders')}),
    )
    readonly_fields = ('slug',)
    filter_horizontal = ('team',)
    list_filter = ('backup_active',)
    list_display = ('name', 'live_url', 'backup_active', 'machine',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'class_type')
    #readonly_fields = ('project', 'date', 'text', 'class_type')

class DomainAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'end_time','registar')}),
    )
    list_display = ('name', 'registar', 'end_time')

class RegistarAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'panel_registar','username_panel_registar','password_panel_registar')}),
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LotrekUser, LotrekUserAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Reseller, ResellerAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Registar, RegistarAdmin)

