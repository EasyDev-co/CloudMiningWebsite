from django.contrib import admin
from src.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'created_at',
        'is_published'
    )
    readonly_fields = [
        'first_name',
        'last_name',
        'phone_number',
        'text',
        'rating',
        'created_at',
        ]
