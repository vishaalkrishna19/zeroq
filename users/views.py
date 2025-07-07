from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, UserAccount
from .serializers import (
    UserSerializer, 
    UserListSerializer,
    UserCreateSerializer,
    UserAccountSerializer,
    UserAccountCreateSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer
)
from .services import EmailService


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides CRUD operations and user management features.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.prefetch_related('useraccount_set__account', 'useraccount_set__role')
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(employee_id__icontains=search)
            )
        
        # Filter by employment status
        employment_status = self.request.query_params.get('employment_status', None)
        if employment_status:
            queryset = queryset.filter(employment_status=employment_status)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        # Filter by account
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            queryset = queryset.filter(useraccount__account_id=account_id)
        
        return queryset.order_by('last_name', 'first_name')
    
    def create(self, request, *args, **kwargs):
        """Override create to handle password generation and email sending."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        user.created_by = request.user
        user.save()
        
        # Print password to terminal if generated
        if hasattr(user, '_generated_password'):
            password = user._generated_password
            
            print("\n" + "="*60)
            print("🔐 NEW USER CREATED VIA API")
            print("="*60)
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.get_full_name()}")
            print(f"Generated Password: {password}")
            print(f"Employee ID: {user.employee_id or 'Not set'}")
            print(f"Created by: {request.user.username}")
            print("⚠️  User must change password on first login")
            print("="*60 + "\n")
            
            # Send email with credentials
            if user.email:
                email_sent = EmailService.send_user_credentials_email(
                    user=user,
                    password=password,
                    created_by=request.user
                )
                
                if email_sent:
                    print("✅ Email sent successfully to user's email address")
                else:
                    print("❌ Failed to send email - check email configuration")
            else:
                print("⚠️  No email address provided - email not sent")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['get'])
    def accounts(self, request, pk=None):
        """Get all accounts for this user."""
        user = self.get_object()
        user_accounts = user.useraccount_set.select_related('account', 'role')
        serializer = UserAccountSerializer(user_accounts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Change user password."""
        user = self.get_object()
        
        # Check if user can change this password
        if request.user != user and not request.user.is_staff:
            return Response(
                {"error": "You can only change your own password."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({"message": "Password changed successfully."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Admin password reset with email notification."""
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can reset passwords."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            force_change = serializer.validated_data['force_change']
            
            user.set_password(new_password)
            user.must_change_password = force_change
            user.save()
            
            # Log password reset
            print(f"\n🔐 PASSWORD RESET by {request.user.username}")
            print(f"Target User: {user.username} ({user.get_full_name()})")
            print(f"Must change on login: {force_change}")
            print(f"Reset at: {timezone.now()}\n")
            
            # Send email notification
            if user.email:
                email_sent = EmailService.send_password_reset_notification(
                    user=user,
                    new_password=new_password,
                    reset_by=request.user
                )
                
                if email_sent:
                    print("✅ Password reset email sent successfully")
                else:
                    print("❌ Failed to send password reset email")
            
            return Response({
                "message": "Password reset successfully.",
                "must_change_password": force_change,
                "email_sent": user.email and email_sent
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a user."""
        user = self.get_object()
        user.is_active = False
        user.employment_status = 'inactive'
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a user."""
        user = self.get_object()
        user.is_active = True
        user.employment_status = 'active'
        user.save()
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserAccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user-account relationships.
    Handles onboarding and offboarding processes.
    """
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserAccountCreateSerializer
        return UserAccountSerializer
    
    def get_queryset(self):
        queryset = UserAccount.objects.select_related('user', 'account', 'role')
        
        # Filter by user
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by account
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        
        # Filter by role
        role_id = self.request.query_params.get('role_id', None)
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by onboarding status
        onboarding_completed = self.request.query_params.get('onboarding_completed', None)
        if onboarding_completed is not None:
            queryset = queryset.filter(onboarding_completed=onboarding_completed.lower() == 'true')
        
        return queryset.order_by('account__account_name', 'user__last_name')
    
    def create(self, request, *args, **kwargs):
        """Override create to set created_by."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_account = serializer.save()
        user_account.created_by = request.user
        user_account.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserAccountSerializer(user_account).data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    @action(detail=True, methods=['post'])
    def start_onboarding(self, request, pk=None):
        """Start onboarding process for user account."""
        user_account = self.get_object()
        user_account.start_onboarding(started_by=request.user)
        
        serializer = self.get_serializer(user_account)
        return Response({
            "message": "Onboarding started successfully.",
            "user_account": serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def complete_onboarding(self, request, pk=None):
        """Complete onboarding process for user account."""
        user_account = self.get_object()
        user_account.complete_onboarding(completed_by=request.user)
        
        serializer = self.get_serializer(user_account)
        return Response({
            "message": "Onboarding completed successfully.",
            "user_account": serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def start_offboarding(self, request, pk=None):
        """Start offboarding process for user account."""
        user_account = self.get_object()
        user_account.start_offboarding(started_by=request.user)
        
        serializer = self.get_serializer(user_account)
        return Response({
            "message": "Offboarding started successfully.",
            "user_account": serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def complete_offboarding(self, request, pk=None):
        """Complete offboarding process for user account."""
        user_account = self.get_object()
        user_account.complete_offboarding(completed_by=request.user)
        
        serializer = self.get_serializer(user_account)
        return Response({
            "message": "Offboarding completed successfully.",
            "user_account": serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def pending_onboarding(self, request):
        """Get all user accounts with pending onboarding."""
        queryset = self.get_queryset().filter(
            onboarding_completed=False,
            is_active=True
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_offboarding(self, request):
        """Get all user accounts with pending offboarding."""
        queryset = self.get_queryset().filter(
            offboarding_started=True,
            offboarding_completed_at__isnull=True
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)