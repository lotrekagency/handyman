from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Project, FrontendTest, Report, LotrekUser, Machine, Reseller, Deadline, Domain
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = '🔩 Handyman'
admin.site.index_title = 'The best Lotrèk\'s friend for backups, monitoring and 🍻'


class DomainResource(resources.ModelResource):

    class Meta:
        model = Domain
        fields = ('url','price','end_time')
        widgets = {
                   'end_time': {'format': '%d/%m/%Y'},
        }


class LotrekUserAdmin(UserAdmin):
    actions = []
    fieldsets = ()
    exclude = ('groups',)
    readonly_fields = ('last_login', 'date_joined',)


    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('last_login', 'date_joined',)
        else:
            return (
                'last_login', 'date_joined',
                'is_active', 'is_staff', 'is_superuser',
                'user_permissions'
            )

    def get_queryset(self, request):
        qs = super(LotrekUserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(id=request.user.id)
        return qs


class FrontendTestInline(admin.TabularInline):
    model = FrontendTest
    extra = 1


class ResellerAdmin(admin.ModelAdmin):
    pass


class DomainAdmin(ImportExportModelAdmin):
    resource_class = DomainResource
    fieldsets = (
        (_('General'), {'fields': ('url','price','end_time')}),
        (_('Service'), {'fields': ('site_on','site_on_backup','mail_on','mail_on_backup')}),
    )
    list_display = ('url', 'price','end_time')
    list_filter = ('site_on','mail_on')
    search_fields = ('url','end_time')
    #search_fields = ('url')


class DeadlineInline(admin.TabularInline):
    model = Deadline
    extra = 1


class MachineAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General'), {'fields': ('name', 'reseller', 'end_time','root_permissions','management_contract','price','price_period','machine_type')}),
        (_('Online Panel'), {'fields': ('administration_panel', 'administration_panel_username', 'administration_panel_password')}),
        (_('Ssh'), {'fields': ('server_address', 'ssh_username', 'ssh_password', 'notes')}),
        
    )
    list_display = ('name', 'server_address', 'reseller', 'end_time')
    list_filter = ('machine_type','management_contract','root_permissions','reseller')
    search_fields = ('name', 'server_address')


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        FrontendTestInline,
        DeadlineInline
    ]
    fieldsets = (
        (_('General'), {'fields': ('name', 'slug', 'live_url', 'team', 'machine', 'ssh_access', 'machine_notes')}),
        (_('Backup'), {'fields': ('backup_active', 'backup_archive', 'backup_script', 'backup_sync_folders')}),
    )
    readonly_fields = ('slug', 'ssh_access', 'machine_notes')
    filter_horizontal = ('team',)
    list_filter = ('backup_active', 'machine')
    list_display = (
        'name', 'slug', 'live_url',
        'backup_active', 'machine',
    )
    search_fields = ('name', 'slug')

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(team__id__in=[request.user.id])
        return qs

    def ssh_access(self, obj):
        if obj.machine:
            return obj.machine.ssh_access

    def machine_notes(self, obj):
        if obj.machine:
            return obj.machine.notes


class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'class_type')
    readonly_fields = ('project', 'date', 'text', 'class_type')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LotrekUser, LotrekUserAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Reseller, ResellerAdmin)
admin.site.register(Domain, DomainAdmin)
