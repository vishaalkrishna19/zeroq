from django.contrib import admin
from django.contrib import messages
from .models import Account, Role, Permission, UserAccount

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    actions = ['activate_accounts', 'deactivate_accounts']
    
    def activate_accounts(self, request, queryset):
        updated = queryset.update(is_active=True)
        messages.success(request, f'{updated} accounts activated successfully')
    activate_accounts.short_description = "Activate selected accounts"
    
    def deactivate_accounts(self, request, queryset):
        updated = queryset.update(is_active=False)
        messages.success(request, f'{updated} accounts deactivated successfully')
    deactivate_accounts.short_description = "Deactivate selected accounts"

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename']
    search_fields = ['name', 'codename']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            messages.success(request, f'Permission "{obj.name}" created successfully')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'is_active', 'created_at']
    list_filter = ['is_active', 'account', 'created_at']
    search_fields = ['name', 'account__name']
    filter_horizontal = ['permissions']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            messages.success(request, f'Role "{obj.name}" created for account "{obj.account.name}"')

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'role', 'is_active', 'joined_at']
    list_filter = ['is_active', 'account', 'role', 'joined_at']
    search_fields = ['user__email', 'account__name']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            messages.success(request, f'User "{obj.user.email}" assigned to account "{obj.account.name}" with role "{obj.role.name}"')
