from rest_framework import serializers
from .models import Account, Role, Permission, UserAccount

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'email', 'phone', 'address', 'website', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'description']

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = UserAccount
        fields = ['id', 'account', 'role', 'is_active', 'joined_at']
        read_only_fields = ['id', 'joined_at']
