from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class JobTitle(models.Model):
    """
    Predefined job titles for users and boarding template mapping.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(
        max_length=100,
        unique=True,
        help_text='Job title name'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Description of the job title and responsibilities'
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text='Primary department for this job title'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this job title is available for selection'
    )
    
    # boarding_template_title = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     help_text='Corresponding boarding template title for onboarding'
    # )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_job_titles',
        help_text='User who created this job title'
    )
    
    class Meta:
        db_table = 'job_titles'
        verbose_name = 'Job Title'
        verbose_name_plural = 'Job Titles'
        ordering = ['title']
        
    def __str__(self):
        return self.title
    
    @property
    def user_count(self):
        """Return number of users with this job title."""
        return self.users.filter(is_active=True).count()


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Handles authentication and basic user information.
    """
    
    # Override the primary key to use UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Enhanced user information
    # employee_id = models.CharField(
    #     max_length=50,
    #     unique=True,
    #     null=True,
    #     blank=True,
    #     help_text='Company employee ID'
    # )
    
    # Profile information removed - keeping minimal user data
    
    # Employment information
    # hire_date = models.DateField(
    #     null=True,
    #     blank=True,
    #     help_text='Date when the employee was hired'
    # )
    template = models.ForeignKey(
        'boarding.JourneyTemplate',  # Use app_label.ModelName as a string
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_users',
        help_text='Journey template assigned to this user'
    )

    termination_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date when the employee was terminated (if applicable)'
    )
    
    # Job information - Updated to use ForeignKey
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text='Current job title'
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Department or team'
    )
    
    # Status tracking
    EMPLOYMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('on_leave', 'On Leave'),
        ('suspended', 'Suspended'),
    ]
    
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default='active',
        help_text='Current employment status'
    )
    
    # Security and access
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    
    # Password management
    password_changed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the password was last changed'
    )
    
    must_change_password = models.BooleanField(
        default=True,
        help_text='Whether user must change password on next login'
    )
    
    # Two-factor authentication
    two_factor_enabled = models.BooleanField(
        default=False,
        help_text='Whether two-factor authentication is enabled'
    )
    
    # Company relationship - One user belongs to one company only
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text='Company this user belongs to'
    )
    
    # Role in the company
    role = models.ForeignKey(
        'roles_permissions.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='User role in the company'
    )
    
    # Admin access for the account
    can_access_admin = models.BooleanField(
        default=False,
        help_text='Whether user can access admin features'
    )
    
    # Custom permissions - Use our custom permission system
    custom_permissions = models.ManyToManyField(
        'roles_permissions.Permission',
        blank=True,
        related_name='users_with_permission',
        help_text='Additional permissions granted directly to this user'
    )
    
    # Audit fields (inherited: date_joined, last_login)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        help_text='User who created this account'
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name', 'username']
        
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.username})"
        return self.username
    
    def get_full_name(self):
        """Return the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_short_name(self):
        """Return the user's short name."""
        return self.first_name or self.username
    
    # @property
    # def is_employed(self):
    #     """Return True if user is currently employed."""
    #     return self.employment_status == 'active' and self.is_active
    
    # @property
    # def days_since_hire(self):
    #     """Return number of days since hire date."""
    #     if self.hire_date:
    #         return (timezone.now().date() - self.hire_date).days
    #     return None
    
    @property
    def account_memberships(self):
        """Return the user's account (now single account)."""
        if self.account:
            return [self.account]
        return []
    
    def get_accounts(self):
        """Return list of accounts this user belongs to (now just one)."""
        if self.account:
            return [self.account]
        return []
    
    def get_primary_account(self):
        """Return the user's account (now always the only account)."""
        return self.account
    
    def has_role_in_account(self, role_name, account):
        """Check if user has a specific role in an account."""
        return (self.account == account and 
                self.role and 
                self.role.name == role_name and 
                self.is_active)
    
    def is_admin_in_account(self, account):
        """Check if user is admin in a specific account."""
        return self.has_role_in_account('admin', account)
    
    def get_permissions_for_account(self, account):
        """Get all permissions for user in a specific account."""
        if self.account == account and self.role and self.is_active:
            return self.role.rolepermission_set.filter(is_granted=True).values_list(
                'permission__codename', flat=True
            )
        return []
    
    def set_password(self, raw_password):
        """Override to track password change time."""
        super().set_password(raw_password)
        self.password_changed_at = timezone.now()
        self.must_change_password = False
    
    # def save(self, *args, **kwargs):
    #     """Override save to ensure proper database transactions."""
    #     # Ensure employee_id is uppercase if provided
    #     if self.employee_id:
    #         self.employee_id = self.employee_id.upper()
        
    #     # Call parent save method
    #     super().save(*args, **kwargs)


class UserAccount(models.Model):
    """
    Through model linking Users to Accounts with roles.
    Represents a user's membership in a company account.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    role = models.ForeignKey('roles_permissions.Role', on_delete=models.SET_NULL, null=True)
    
    # Membership details
    is_primary = models.BooleanField(
        default=False,
        help_text='Whether this is the user\'s primary account'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this account membership is active'
    )
    
    # Access control
    can_access_admin = models.BooleanField(
        default=False,
        help_text='Whether user can access admin features for this account'
    )
    
    # Onboarding/Offboarding tracking
    onboarding_completed = models.BooleanField(
        default=False,
        help_text='Whether onboarding process is completed'
    )
    
    onboarding_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When onboarding was completed'
    )
    
    offboarding_started = models.BooleanField(
        default=False,
        help_text='Whether offboarding process has started'
    )
    
    offboarding_started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When offboarding was started'
    )
    
    offboarding_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When offboarding was completed'
    )
    
    # Notes and metadata
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about this user account relationship'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_user_accounts',
        help_text='User who created this account membership'
    )
    
    class Meta:
        db_table = 'user_accounts'
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        unique_together = ['user', 'account']
        ordering = ['account__account_name', 'user__last_name', 'user__first_name']
        
    def __str__(self):
        return f"{self.user.get_full_name()} @ {self.account.account_name} ({self.role})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure only one primary account per user
        if self.is_primary:
            existing_primary = UserAccount.objects.filter(
                user=self.user,
                is_primary=True
            ).exclude(pk=self.pk)
            
            if existing_primary.exists():
                raise ValidationError('User can only have one primary account.')
    
    def save(self, *args, **kwargs):
        """Override save to ensure validation and proper database transactions."""
        # Call clean method for validation
        self.clean()
        
        # Call parent save method
        super().save(*args, **kwargs)
    
    @property
    def is_onboarded(self):
        """Return True if user is fully onboarded."""
        return self.onboarding_completed and self.is_active
    
    @property
    def is_offboarded(self):
        """Return True if user is offboarded."""
        return self.offboarding_completed_at is not None
    
    @property
    def onboarding_status(self):
        """Return current onboarding status."""
        if self.onboarding_completed:
            return 'completed'
        elif self.is_active:
            return 'in_progress'
        else:
            return 'not_started'
    
    @property
    def offboarding_status(self):
        """Return current offboarding status."""
        if self.offboarding_completed_at:
            return 'completed'
        elif self.offboarding_started:
            return 'in_progress'
        else:
            return 'not_started'
    
    def start_onboarding(self, started_by=None):
        """Start the onboarding process."""
        self.is_active = True
        self.save()
        # Here you would trigger onboarding workflows
    
    def complete_onboarding(self, completed_by=None):
        """Mark onboarding as completed."""
        self.onboarding_completed = True
        self.onboarding_completed_at = timezone.now()
        self.save()
    
    def start_offboarding(self, started_by=None):
        """Start the offboarding process."""
        self.offboarding_started = True
        self.offboarding_started_at = timezone.now()
        self.save()
        # Here you would trigger offboarding workflows
    
    def complete_offboarding(self, completed_by=None):
        """Complete the offboarding process."""
        self.offboarding_completed_at = timezone.now()
        self.is_active = False
        self.user.employment_status = 'terminated'
        self.user.save()
        self.save()