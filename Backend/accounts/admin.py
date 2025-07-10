from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'account_name', 
        
        'timezone', 
        'user_count',
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
        'created_at', 
        'updated_at', 
        'user_count'
    ]
    
    fieldsets = (
        ('Basic Information', {
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
        ('Account Settings', {
            'fields': (
                'max_users',
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
    
    def save_model(self, request, obj, form, change):
        """Override to ensure account data is properly saved."""
        try:
            # Save the account
            super().save_model(request, obj, form, change)
            
            # Verify the save was successful
            obj.refresh_from_db()
            
            action = "created" if not change else "updated"
            print(f"✅ Account {action}: {obj.account_name}")
            
        except Exception as e:
            print(f"❌ Error saving Account: {e}")
            raise
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()