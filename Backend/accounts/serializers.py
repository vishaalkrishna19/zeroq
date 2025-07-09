from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    user_count = serializers.ReadOnlyField()
    can_add_users = serializers.ReadOnlyField()
    
    class Meta:
        model = Account
        fields = [
            'id', 
            'account_name', 
            'timezone', 
            'is_active',
            'contact_email', 
            'contact_phone',
            'address_line1', 
            'address_line2', 
            'city', 
            'state', 
            'postal_code', 
            'country',
            'max_users',
            'user_count', 
            'can_add_users',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccountListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing accounts."""
    user_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Account
        fields = [
            'id', 
            'account_name', 
            'timezone', 
            'is_active',
            'user_count',
            'created_at'
        ]