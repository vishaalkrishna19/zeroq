from django.db import models
from django.utils import timezone
import uuid

class Account(models.Model):
    """Company/Organization account"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    
    def __str__(self):
        return self.name

class Permission(models.Model):
    """System permissions"""
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'permissions'
    
    def __str__(self):
        return self.name

class Role(models.Model):
    """User roles within an account"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'roles'
        unique_together = ['account', 'name']
    
    def __str__(self):
        return f"{self.account.name} - {self.name}"

class UserAccount(models.Model):
    """Junction table for user-account relationships"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'user_accounts'
        unique_together = ['user', 'account']
    
    def __str__(self):
        return f"{self.user.email} - {self.account.name}"
