from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from .models import Violation, Violator, ViolationRecord


class ViolationResource(ModelResource):
    class Meta:
        model = Violation


class ViolatorResource(ModelResource):
    class Meta:
        model = Violator


class ViolationRecordResource(ModelResource):
    class Meta:
        model = ViolationRecord


class ViolationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ViolationResource
    list_display = ('code', 'legal_basis', 'date_created',
                    'date_updated', 'driver_fine', 'owner_fine', 'eu_code', 'is_active')
    search_fields = ('code', 'legal_basis', 'eu_code')
    list_filter = ('date_created', 'date_updated', 'is_active')


class ViolatorAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ViolatorResource
    list_display = ('circulation_number', 'name')
    search_fields = ('circulation_number', 'name')
    list_filter = ('name',)


class ViolationRecordAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ViolationRecordResource
    list_display = ('violator', 'violation', 'datetime_inspection',
                    'kind_violator', 'fine_amount')
    search_fields = ('violator__license_number', 'violation__code')
    list_filter = ('kind_violator', 'datetime_inspection', 'violation__code')


admin.site.register(Violation, ViolationAdmin)
admin.site.register(Violator, ViolatorAdmin)
admin.site.register(ViolationRecord, ViolationRecordAdmin)
