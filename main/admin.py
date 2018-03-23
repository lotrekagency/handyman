from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, FrontendTest, Report, LotrekUser, Machine, Reseller, Deadline, Domain, Registar, Certificate, Certificateseller, Domainregistrant, Customer, Payment

from .actions import export_as_csv_action, put_googleevent


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
        (_('General'), {'fields': ('name', 'name_on_reseller', 'end_time','root_permissions','management_contract','price')}),
        (_('Reseller'), {'fields': ('reseller', 'reseller_panel', 'reseller_panel_username', 'reseller_panel_password')}),
        (_('Ssh'), {'fields': ('server_address', 'ssh_username', 'ssh_password')}),
        (_('Online panel'), {'fields': ('online_panel', 'online_panel_username', 'online_panel_password')}),
    )
    search_fields = ('name','server_address')
    list_filter = ('reseller',)
    list_display = ('name', 'server_address', 'root_permissions','management_contract', 'price','reseller', 'end_time')
    #actions = [openterminal("ssh open", fields=['server_address','ssh_username','ssh_password'])]

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




class DomainregistrantAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {'fields': ('name','email')}),
    )
    #readonly_fields = ('project', 'date', 'text', 'class_type')    

class DomainAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'price','end_time','own','registar','registrant','to_renew')}),
    )
    search_fields = ('name',)
    list_filter = ('registrant','registar','own','end_time',)
    list_display = ('name', 'own','price','registar','registrant', 'end_time','to_renew')
    actions = [export_as_csv_action("CSV Export", fields=['name','price'])]

class RegistarAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'panel_registar','username_panel_registar','password_panel_registar')}),
    )


class CertificateAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'end_time','customer','seller')}),
    )
    search_fields = ('name',)
    list_filter = ('customer',)
    list_display = ('name', 'end_time','customer')


class CertificatesellerAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('General'), {'fields': ('name', 'panel_seller','username_panel_seller','password_panel_seller')}),
    )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class PaymentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {'fields': ('name','paid', 'customer','price','note','machines','domains','certificates','start_time','end_time','month')}),
    )
    search_fields = ('name',)
    filter_horizontal = ('domains','machines','certificates',)
    list_filter = ('paid',)
    list_display = ('name', 'customer','price','month','start_time','end_time','paid')


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
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Payment, PaymentAdmin)

