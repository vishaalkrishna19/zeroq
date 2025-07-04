from django.db import models
from django.core.validators import RegexValidator
import uuid


class Account(models.Model):
    """
    Represents a company/organization account that uses the application.
    Each account can have multiple users and maintains its own timezone settings.
    """
    
    # Unique identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9]{3,20}$',
            message='Account ID must be 3-20 characters, uppercase letters and numbers only'
        )],
        help_text='Unique account identifier (e.g., COMP001, ACME123)'
    )
    
    # Basic account information
    account_name = models.CharField(
        max_length=255,
        help_text='Full company/organization name'
    )
    
    # Timezone configuration
    TIMEZONE_CHOICES = [
        ('UTC', 'UTC'),
        ('US/Eastern', 'US/Eastern'),
        ('US/Central', 'US/Central'),
        ('US/Mountain', 'US/Mountain'),
        ('US/Pacific', 'US/Pacific'),
        ('Europe/London', 'Europe/London'),
        ('Europe/Paris', 'Europe/Paris'),
        ('Asia/Tokyo', 'Asia/Tokyo'),
        ('Asia/Shanghai', 'Asia/Shanghai'),
        ('Asia/Kolkata', 'Asia/Kolkata'),
        ('Australia/Sydney', 'Australia/Sydney'),
    ]
    
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='UTC',
        help_text='Primary timezone for this account'
    )
    
    # Account status and metadata
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this account is currently active'
    )
    
    # Contact information
    contact_email = models.EmailField(
        blank=True,
        null=True,
        help_text='Primary contact email for this account'
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Primary contact phone number'
    )
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default='United States')
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Account settings
    max_users = models.PositiveIntegerField(
        default=100,
        help_text='Maximum number of users allowed for this account'
    )
    
    subscription_type = models.CharField(
        max_length=50,
        choices=[
            ('trial', 'Trial'),
            ('basic', 'Basic'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        default='trial'
    )
    
    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['account_name']
        
    def __str__(self):
        return f"{self.account_name} ({self.account_id})"
    
    def save(self, *args, **kwargs):
        # Ensure account_id is uppercase
        if self.account_id:
            self.account_id = self.account_id.upper()
        super().save(*args, **kwargs)
    
    @property
    def user_count(self):
        """Returns the current number of users associated with this account."""
        return self.useraccount_set.filter(user__is_active=True).count()
    
    @property
    def can_add_users(self):
        """Returns True if the account can add more users."""
        return self.user_count < self.max_users
    
    def get_active_users(self):
        """Returns queryset of active users for this account."""
        from users.models import User
        return User.objects.filter(
            useraccount__account=self,
            is_active=True
        ).select_related('useraccount')
    
    def get_admin_users(self):
        """Returns queryset of admin users for this account."""
        from users.models import User
        from roles_permissions.models import Role
        
        admin_role = Role.objects.filter(name='admin').first()
        if not admin_role:
            return User.objects.none()
            
        return User.objects.filter(
            useraccount__account=self,
            useraccount__role=admin_role,
            is_active=True
        ).select_related('useraccount')