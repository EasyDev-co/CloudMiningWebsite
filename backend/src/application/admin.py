from django.contrib import admin
from src.application.models import MaintenanceCost


@admin.register(MaintenanceCost)
class MaintenanceCostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'coast'
    )
    readonly_fields = ['id']
