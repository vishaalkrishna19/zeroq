from rest_framework import serializers
from .models import Permission, Role, RolePermission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id', 
            'name', 
            'codename', 
            'description', 
            'category', 
            'level', 
            'is_active',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RolePermissionSerializer(serializers.ModelSerializer):
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    permission_category = serializers.CharField(source='permission.category', read_only=True)
    permission_level = serializers.CharField(source='permission.level', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = [
            'id',
            'permission',
            'permission_name',
            'permission_category', 
            'permission_level',
            'is_granted',
            'constraints',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RoleSerializer(serializers.ModelSerializer):
    permissions_detail = RolePermissionSerializer(
        source='rolepermission_set', 
        many=True, 
        read_only=True
    )
    permission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = [
            'id', 
            'name', 
            'display_name', 
            'description', 
            'level', 
            'is_system_role',
            'is_default',
            'is_active',
            'permission_count',
            'permissions_detail',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_permission_count(self, obj):
        return obj.rolepermission_set.filter(is_granted=True).count()
    
    def validate(self, data):
        # Prevent modification of system roles
        if self.instance and self.instance.is_system_role:
            if 'name' in data and data['name'] != self.instance.name:
                raise serializers.ValidationError("Cannot modify name of system roles.")
            if 'is_system_role' in data and not data['is_system_role']:
                raise serializers.ValidationError("Cannot remove system role status.")
        
        return data


class RoleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing roles."""
    permission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = [
            'id', 
            'name', 
            'display_name', 
            'level', 
            'is_system_role',
            'is_default',
            'is_active',
            'permission_count'
        ]
    
    def get_permission_count(self, obj):
        return obj.rolepermission_set.filter(is_granted=True).count()


class AssignPermissionSerializer(serializers.Serializer):
    """Serializer for assigning/removing permissions to/from roles."""
    permission_id = serializers.UUIDField()
    is_granted = serializers.BooleanField(default=True)
    constraints = serializers.JSONField(required=False, default=dict)
    
    def validate_permission_id(self, value):
        try:
            Permission.objects.get(id=value, is_active=True)
        except Permission.DoesNotExist:
            raise serializers.ValidationError("Permission not found or inactive.")
        return value