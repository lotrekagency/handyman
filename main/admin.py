from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, FrontendTest, Report, LotrekUser, Machine, Reseller, Deadline, Domain, Registar, Certificate, Certificateseller, Domainregistrant

from .actions import export_as_csv_action


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
        (_('General'), {'fields': ('name', 'name_on_reseller', 'end_time','root_permissions')}),
        (_('Reseller'), {'fields': ('reseller', 'reseller_panel', 'reseller_panel_username', 'reseller_panel_password')}),
        (_('Ssh'), {'fields': ('server_address', 'ssh_username', 'ssh_password')}),
        (_('Online panel'), {'fields': ('online_panel', 'online_panel_username', 'online_panel_password')}),
    )
    list_display = ('name', 'server_address', 'root_permissions', 'reseller', 'end_time')


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

def export_products(self, request, queryset):
    meta = {
            'file': '/tmp/products.csv',
            'queryset': queryset,
            'fields': ('name','price')
        }
    return get_model_as_csv_file_response(meta, content_type='text/csv')
export_products.short_description = 'Export as csv'


class DomainregistrantAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {'fields': ('name','email')}),
    )
    #readonly_fields = ('project', 'date', 'text', 'class_type')    

class DomainAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'price','end_time','own','registar','registrant')}),
    )
    list_filter = ('registrant',)
    list_display = ('name', 'own','price','registar','registrant', 'end_time')
    actions = [export_as_csv_action("CSV Export", fields=['name','price'])]

class RegistarAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'panel_registar','username_panel_registar','password_panel_registar')}),
    )


class CertificateAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'end_time','seller')}),
    )


class CertificatesellerAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'panel_seller','username_panel_seller','password_panel_seller')}),
    )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LotrekUser, LotrekUserAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Reseller, ResellerAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Registar, RegistarAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Certificateseller, CertificatesellerAdmin)
admin.site.register(Domainregistrant, DomainregistrantAdmin)

