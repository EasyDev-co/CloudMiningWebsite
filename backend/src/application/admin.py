from django.contrib import admin
from src.application.models import (
    MaintenanceCost,
    Contract,
    RentalThCost
)


@admin.register(MaintenanceCost)
class MaintenanceCostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cost'
    )
    readonly_fields = ['id']


@admin.register(RentalThCost)
class RentalThCostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cost'
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
