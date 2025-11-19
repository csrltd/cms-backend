from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'full_name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )
