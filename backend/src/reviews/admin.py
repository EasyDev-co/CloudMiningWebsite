from django.contrib import admin
from src.reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'text',
        'created_at',
        'is_published'
    )
    readonly_fields = ['author', 'text', 'created_at']
