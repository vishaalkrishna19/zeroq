from django.contrib import admin
from django.utils.html import format_html
from .models import Permission, Role, RolePermission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'codename', 
        'category', 
        'level', 
        'is_active', 
        'created_at'
    ]
    
    list_filter = [
        'category', 
        'level', 
        'is_active', 
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'codename', 
        'description'
    ]
    
    readonly_fields = [
        'id', 
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 
                'codename', 
                'description'
            )
        }),
        ('Classification', {
            'fields': (
                'category', 
                'level', 
                'is_active'
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
    
    ordering = ['category', 'level', 'name']
    
    def save_model(self, request, obj, form, change):
        """Override to ensure permission data is properly saved."""
        try:
            # Save the permission
            super().save_model(request, obj, form, change)
            
            # Verify the save was successful
            obj.refresh_from_db()
            
            action = "created" if not change else "updated"
            print(f"✅ Permission {action}: {obj.name} ({obj.codename})")
            
        except Exception as e:
            print(f"❌ Error saving Permission: {e}")
            raise


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 0
    fields = ['permission', 'is_granted', 'constraints']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('permission')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
        'display_name', 
        'name', 
        'level', 
        'permission_count',
        'is_system_role',
        'is_default',
        'is_active', 
        'created_at'
    ]
    
    list_filter = [
        'level', 
        'is_system_role',
        'is_default',
        'is_active', 
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'display_name', 
        'description'
    ]
    
    readonly_fields = [
        'id', 
        'permission_count',
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 
                'display_name', 
                'description'
            )
        }),
        ('Role Settings', {
            'fields': (
                'level', 
                'is_system_role',
                'is_default',
                'is_active'
            )
        }),
        ('Metadata', {
            'fields': (
                'id', 
                'permission_count',
                'created_at', 
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RolePermissionInline]
    ordering = ['level', 'name']
    
    def permission_count(self, obj):
        count = obj.rolepermission_set.filter(is_granted=True).count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'red',
            count
        )
    permission_count.short_description = 'Permissions'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('rolepermission_set')
    
    def save_model(self, request, obj, form, change):
        """Override to ensure role data is properly saved."""
        try:
            # Save the role
            super().save_model(request, obj, form, change)
            
            # Verify the save was successful
            obj.refresh_from_db()
            
            action = "created" if not change else "updated"
            print(f"✅ Role {action}: {obj.name}")
            
        except Exception as e:
            print(f"❌ Error saving Role: {e}")
            raise


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = [
        'role', 
        'permission', 
        'permission_category',
        'permission_level',
        'is_granted_display', 
        'created_at'
    ]
    
    list_filter = [
        'is_granted', 
        'permission__category', 
        'permission__level',
        'role__name',
        'created_at'
    ]
    
    search_fields = [
        'role__name', 
        'permission__name', 
        'permission__codename'
    ]
    
    readonly_fields = [
        'id', 
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Assignment', {
            'fields': (
                'role', 
                'permission', 
                'is_granted'
            )
        }),
        ('Additional Settings', {
            'fields': (
                'constraints',
                'created_by'
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
    
    ordering = ['role__name', 'permission__category', 'permission__name']
    
    def permission_category(self, obj):
        return obj.permission.category
    permission_category.short_description = 'Category'
    
    def permission_level(self, obj):
        return obj.permission.level
    permission_level.short_description = 'Level'
    
    def is_granted_display(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'green' if obj.is_granted else 'red',
            '✓ Granted' if obj.is_granted else '✗ Denied'
        )
    is_granted_display.short_description = 'Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('role', 'permission')