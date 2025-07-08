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
    PasswordChangeSerializer
)
from .services import EmailService
<<<<<<< Updated upstream
=======
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
>>>>>>> Stashed changes


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
        queryset = User.objects.select_related('account', 'role')
        
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
            queryset = queryset.filter(account_id=account_id)
        
        return queryset.order_by('last_name', 'first_name')
    
    def create(self, request, *args, **kwargs):
        """Override create to handle password generation and logging."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        user.created_by = request.user
        user.save()
        
        # Print password to terminal if generated
        if hasattr(user, '_generated_password'):
            password= user._generated_password
            print("\n" + "="*60)
            print("🔐 NEW USER CREATED VIA API")
            print("="*60)
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.get_full_name()}")
            print(f"Generated Password: {user._generated_password}")
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
                    print(":white_check_mark: Email sent successfully to user's email address")
                else:
                    print(":x: Failed to send email - check email configuration")
            else:
                print(":warning:  No email address provided - email not sent")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['get'])
    def account(self, request, pk=None):
        """Get account information for this user."""
        user = self.get_object()
        if user.account:
            from accounts.serializers import AccountSerializer
            serializer = AccountSerializer(user.account)
            return Response(serializer.data)
        else:
            return Response({"message": "User is not assigned to any account."}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """Reset current user's password with current password verification."""
        user = request.user
        
        # Get passwords from request
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        # Validate input
        if not current_password or not new_password:
            return Response({
                "error": "Both current_password and new_password are required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify current password
        if not user.check_password(current_password):
            return Response({
                "error": "Current password is incorrect."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate new password (same as current)
        if current_password == new_password:
            return Response({
                "error": "New password must be different from current password."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Set new password
            user.set_password(new_password)
            user.must_change_password = False
            user.password_changed_at = timezone.now()
            user.save()
            
            # Verify the password was set correctly
            user.refresh_from_db()
            if not user.check_password(new_password):
                raise Exception("Password verification failed after save")
            
            # Log password reset
            print(f"\n🔐 PASSWORD RESET by user: {user.username}")
            print(f"Email: {user.email}")
            print(f"Reset at: {timezone.now()}")
            print(f"New password verification: ✅")
            print(f"Database save: ✅\n")
            
            # Send email notification
            if user.email:
                email_sent = EmailService.send_password_reset_notification(
                    user=user,
                    new_password=new_password,
                    reset_by=request.user
                )
                if email_sent:
                    print(":white_check_mark: Password reset email sent successfully")
                else:
                    print(":x: Failed to send password reset email")

            return Response({
                "message": "Password reset successfully.",
                "user": user.username,
                "email_sent":user.email and email_sent,
                "timestamp": timezone.now()
            })
            
        except Exception as e:
            print(f"❌ Error during password reset: {e}")
            return Response({
                "error": "Failed to reset password. Please try again."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def admin_reset_password(self, request, pk=None):
        """Admin password reset for any user."""
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can reset other users' passwords."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({
                "error": "new_password is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Set new password
            user.set_password(new_password)
            user.must_change_password = True  # Force user to change on next login
            user.save()
            
            # Verify the password was set correctly
            user.refresh_from_db()
            if not user.check_password(new_password):
                raise Exception("Password verification failed after save")
            
            # Log password reset
            print(f"\n🔐 ADMIN PASSWORD RESET by {request.user.username}")
            print(f"Target User: {user.username} ({user.get_full_name()})")
            print(f"New Password: {new_password}")
            print(f"Reset at: {timezone.now()}")
            print(f"Must change on login: ✅")
            print(f"Database save verification: ✅\n")
            
            return Response({
                "message": f"Password reset successfully for {user.get_full_name()}.",
                "target_user": user.username,
                "must_change_password": True,
                "timestamp": timezone.now()
            })
            
        except Exception as e:
            print(f"❌ Error during admin password reset: {e}")
            return Response({
                "error": "Failed to reset password. Please try again."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
<<<<<<< Updated upstream
        return Response(serializer.data)
=======
        return Response(serializer.data)

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    """
    Custom login view that checks must_change_password status.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            "error": "Username and password are required."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to get user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "error": "Invalid username or password."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user is active
    if not user.is_active:
        return Response({
            "error": "User account is inactive."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify password
    if not user.check_password(password):
        return Response({
            "error": "Invalid username or password."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user must change password
    if user.must_change_password:
        return Response({
            "must_reset_password": True,
            "message": "You must reset your password before logging in.",
            "username": username,
            "redirect_url": "/enter-key"
        }, status=status.HTTP_200_OK)
    
    # If password doesn't need to be changed, proceed with normal login
    # Authenticate and create session/token
    from django.contrib.auth import authenticate, login
    from rest_framework.authtoken.models import Token
    
    authenticated_user = authenticate(request, username=username, password=password)
    if authenticated_user:
        login(request, authenticated_user)
        
        # Get or create auth token
        token, created = Token.objects.get_or_create(user=authenticated_user)
        
        # Update last login IP
        user.last_login_ip = request.META.get('REMOTE_ADDR')
        user.save(update_fields=['last_login_ip'])
        
        return Response({
            "message": "Login successful",
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "token": token.key,
            "must_reset_password": False
        }, status=status.HTTP_200_OK)
    
    return Response({
        "error": "Authentication failed."
    }, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> Stashed changes
