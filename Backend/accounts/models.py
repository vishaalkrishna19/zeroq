from django.db import models
import uuid


class Account(models.Model):
    """
    Represents a company/organization account that uses the application.
    Each account can have multiple users and maintains its own timezone settings.
    """
    
    # Unique identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
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
    
    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['account_name']
        
    def __str__(self):
        return self.account_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    @property
    def user_count(self):
        """Returns the current number of users associated with this account."""
        return self.users.filter(is_active=True).count()
    
    @property
    def can_add_users(self):
        """Returns True if the account can add more users."""
        return self.user_count < self.max_users
    
    def get_active_users(self):
        """Returns queryset of active users for this account."""
        return self.users.filter(is_active=True)
    
    def get_admin_users(self):
        """Returns queryset of admin users for this account."""
        from roles_permissions.models import Role
        
        admin_role = Role.objects.filter(name='admin').first()
        if not admin_role:
            return self.users.none()
            
        return self.users.filter(
            role=admin_role,
            is_active=True
        )