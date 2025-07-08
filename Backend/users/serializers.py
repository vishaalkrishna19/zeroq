from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserAccount
from .admin import generate_strong_password


class UserSerializer(serializers.ModelSerializer):
    """Full User serializer with all fields."""
    
    account_count = serializers.SerializerMethodField()
    is_employed = serializers.ReadOnlyField()
    days_since_hire = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'employee_id', 'phone_number', 'date_of_birth',
            'hire_date', 'termination_date', 'job_title', 'department',
            'manager', 'employment_status', 'is_active', 'is_staff',
            'is_superuser', 'is_system_admin', 'last_login_ip',
            'must_change_password', 'two_factor_enabled',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'account_count', 'is_employed',
            'days_since_hire', 'date_joined', 'last_login', 'updated_at'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'updated_at',
            'password_changed_at', 'account_count', 'is_employed',
            'days_since_hire'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_account_count(self, obj):
        # User now has only one account, return 1 if account exists, 0 otherwise
        return 1 if obj.account else 0


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight User serializer for listing."""
    
    account_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'employee_id',
            'job_title', 'department', 'employment_status',
            'is_active', 'account_count', 'date_joined'
        ]
    
    def get_account_count(self, obj):
        # User now has only one account, return 1 if account exists, 0 otherwise  
        return 1 if obj.account else 0
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users with auto-generated passwords."""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'employee_id', 'phone_number', 'date_of_birth',
            'hire_date', 'job_title', 'department', 'manager',
            'employment_status', 'is_active', 'is_staff',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country'
        ]
    
    def create(self, validated_data):
        # Generate strong password
        password = generate_strong_password()
        
        # Create user
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        user.must_change_password = True  # Ensure this is set
        user.save()
        
        # Store password for terminal output
        user._generated_password = password
        
        return user


class UserAccountSerializer(serializers.ModelSerializer):
    """Full UserAccount serializer."""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    account_name = serializers.CharField(source='account.account_name', read_only=True)
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    onboarding_status = serializers.ReadOnlyField()
    offboarding_status = serializers.ReadOnlyField()
    
    class Meta:
        model = UserAccount
        fields = [
            'id', 'user', 'account', 'role', 'user_name', 'account_name',
            'role_name', 'is_primary', 'is_active', 'can_access_admin',
            'onboarding_completed', 'onboarding_completed_at',
            'offboarding_started', 'offboarding_started_at',
            'offboarding_completed_at', 'notes', 'onboarding_status',
            'offboarding_status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'onboarding_completed_at', 'offboarding_started_at',
            'offboarding_completed_at', 'created_at', 'updated_at'
        ]


class UserAccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating UserAccount relationships."""
    
    class Meta:
        model = UserAccount
        fields = [
            'user', 'account', 'role', 'is_primary', 'is_active',
            'can_access_admin', 'notes'
        ]
    
    def validate(self, data):
        # Check if user already has membership in this account
        if UserAccount.objects.filter(
            user=data['user'], 
            account=data['account']
        ).exists():
            raise serializers.ValidationError(
                "User already has membership in this account."
            )
        
        # Check if setting as primary when user already has primary account
        if data.get('is_primary'):
            existing_primary = UserAccount.objects.filter(
                user=data['user'],
                is_primary=True
            ).exists()
            
            if existing_primary:
                raise serializers.ValidationError(
                    "User already has a primary account. Only one primary account allowed."
                )
        
        return data


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for admin password reset."""
    
    new_password = serializers.CharField(required=True)
    force_change = serializers.BooleanField(default=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value