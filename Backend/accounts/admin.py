from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'account_name',
        'timezone',
        'user_count',
        'max_users',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'timezone',
        'created_at'
    ]
    
    search_fields = [
        'account_name',
        'contact_email'
    ]
    
    readonly_fields = [
        'id',
        'user_count',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Account Information', {
            'fields': (
                'account_name',
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
        ('Settings', {
            'fields': (
                'max_users',
                'user_count'
            )
        }),
        ('Metadata', {
            'fields': (
                'id',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['account_name']
    
    def user_count(self, obj):
        return obj.user_count
    user_count.short_description = 'Active Users'