from django.contrib import admin
from .models import Violation, Violator, ViolationRecord


class ViolationAdmin(admin.ModelAdmin):
    list_display = ('code', 'legal_basis', 'date_created',
                    'date_updated', 'driver_fine', 'owner_fine', 'eu_code', 'is_active')
    search_fields = ('code', 'legal_basis', 'eu_code')
    list_filter = ('date_created', 'date_updated', 'is_active')


class ViolatorAdmin(admin.ModelAdmin):
    list_display = ('circulation_number', 'name')
    search_fields = ('circulation_number', 'name')
    list_filter = ('name',)


class ViolationRecordAdmin(admin.ModelAdmin):
    list_display = ('violator', 'violation', 'datetime_inspection',
                    'date_recorded', 'kind_violator', 'fine_amount')
    search_fields = ('violator__license_number', 'violation__code')
    list_filter = ('kind_violator', 'date_recorded', 'violation__code')


admin.site.register(Violation, ViolationAdmin)
admin.site.register(Violator, ViolatorAdmin)
admin.site.register(ViolationRecord, ViolationRecordAdmin)
