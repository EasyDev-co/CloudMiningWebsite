from django.contrib import admin
from src.application.models import MaintenanceCost, Contract


@admin.register(MaintenanceCost)
class MaintenanceCostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'coast'
    )
    readonly_fields = ['id']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'hashrate',
        'contract_start',
        'contract_end',
        'is_paid'
    )
    readonly_fields = ['customer']
