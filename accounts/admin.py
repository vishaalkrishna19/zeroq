from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'account_name', 
        'account_id', 
        'timezone', 
        'subscription_type',
        'user_count',
        'is_active', 
        'created_at'
    ]
    
    list_filter = [
        'is_active', 
        'subscription_type', 
        'timezone', 
        'created_at'
    ]
    
    search_fields = [
        'account_name', 
        'account_id', 
        'contact_email'
    ]
    
    readonly_fields = [
        'id', 
        'created_at', 
        'updated_at', 
        'user_count'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'account_name', 
                'account_id', 
                'timezone', 
                'is_active'
            )
        }),
        ('Contact Information', {
            'fields': (
                'contact_email', 
                'contact_phone'
            )
        }),
        ('Address', {
            'fields': (
                'address_line1', 
                'address_line2', 
                'city', 
                'state', 
                'postal_code', 
                'country'
            ),
            'classes': ('collapse',)
        }),
        ('Account Settings', {
            'fields': (
                'max_users', 
                'subscription_type'
            )
        }),
        ('Metadata', {
            'fields': (
                'id', 
                'user_count', 
                'created_at', 
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['account_name']
    
    def get_queryset(self, request):
        return super().get_queryset(request)