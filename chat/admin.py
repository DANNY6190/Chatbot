from django.contrib import admin

# Register your models here.
from .models import Chat

@admin.register(Chat)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'message',
        'response',
        'created_at',
    )
    list_display_links = ['id']
    search_fields = ['message', 'response', 'created_at']
    ordering = ['created_at']
    list_per_page = 10
    list_max_show_all = 10
    