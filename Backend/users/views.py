from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils import timezone
from dj_rest_auth.views import LoginView
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
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse


class CustomLoginView(LoginView):
    """
    Custom login view that prevents login with temporary password.
    Forces users to go through password reset flow if must_change_password is True.
    """
    
    def post(self, request, *args, **kwargs):
        # Get credentials from request
        username = request.data.get('username')
        password = request.data.get('password')
        is_email=True
        if username and password:
            is_email = True
            try:
                validate_email(username)
            except ValidationError:
                is_email = False
            try:
                if is_email==True:
                    user = User.objects.get(email=username)
                    # Check if user exists and password is correct
                    if user.check_password(password) and user.is_active:
                        # If user must change password, prevent login and redirect to reset flow
                        if user.must_change_password:
                            return Response({
                                "error": "You must change your password before logging in.",
                                "must_reset_password": True,
                                "redirect_url": "/set-password"
                            }, status=status.HTTP_403_FORBIDDEN)
                        
                elif is_email==False:
                    user = User.objects.get(username=username)
                    # Check if user exists and password is correct
                    if user.check_password(password) and user.is_active:
                        # If user must change password, prevent login and redirect to reset flow
                        if user.must_change_password:
                            return Response({
                                "error": "You must change your password before logging in.",
                                "must_reset_password": True,
                                "redirect_url": "/set-password"
                            }, status=status.HTTP_403_FORBIDDEN)
            except User.DoesNotExist:
                pass  # Let default authentication handle the error   
        
       
        
        # If no must_change_password issue, proceed with normal login
        return super().post(request, *args, **kwargs)



class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides CRUD operations and user management features.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Override permissions for specific actions."""
        if self.action == 'reset_password':
            # Allow unauthenticated access for password reset
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
    
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
                Q(email__icontains=search) 
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
    
    # @action(detail=False, methods=['post'])
    # def reset_password(self, request):
    #     """Reset user's password with username and current password verification."""
    #     # Get credentials from request
    #     username = request.data.get('username')
    #     current_password = request.data.get('current_password')
    #     new_password = request.data.get('new_password')
        

        
    #     print(f"🔐 Password reset attempt for username: {username}")
        
    #     # Validate input
    #     if not username or not current_password or not new_password:
    #         return Response({
    #             "error": "Username, current_password, and new_password are required."
    #         }, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Try to authenticate user with username and current password
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return Response({
    #             "error": "Invalid username or password."
    #         }, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Verify current password
    #     if not user.check_password(current_password):
    #         return Response({
    #             "error": "Invalid username or password."
    #         }, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Check if user is active
    #     if not user.is_active:
    #         return Response({
    #             "error": "User account is inactive."
    #         }, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Validate new password (same as current)
    #     if current_password == new_password:
    #         return Response({
    #             "error": "New password must be different from current password."
    #         }, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         # Set new password
    #         user.set_password(new_password)
    #         user.must_change_password = False
    #         user.password_changed_at = timezone.now()
    #         user.save()
            
    #         # Verify the password was set correctly
    #         user.refresh_from_db()
    #         if not user.check_password(new_password):
    #             raise Exception("Password verification failed after save")
            
    #         # Log password reset
    #         print(f"\n🔐 PASSWORD RESET by user: {user.username}")
    #         print(f"Email: {user.email}")
    #         print(f"Reset at: {timezone.now()}")
    #         print(f"New password verification: ✅")
    #         print(f"Database save: ✅\n")
            
    #         return Response({
    #             "message": "Password reset successfully.",
    #             "user": user.username,
    #             "timestamp": timezone.now(),
    #             "success": True
    #         })
            
    #     except Exception as e:
    #         print(f"❌ Error during password reset: {e}")
    #         return Response({
    #             "error": "Failed to reset password. Please try again."
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """Reset user's password with username or email and current password verification."""
        username_or_email = request.data.get('username')
        current_password   = request.data.get('current_password')
        new_password       = request.data.get('new_password')

        print(f"🔐 Password reset attempt for identifier: {username_or_email}")

        # Validate input
        if not username_or_email or not current_password or not new_password:
            return Response({
                "error": "username (or email), current_password, and new_password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Determine whether this is an email or a username
        is_email = True
        try:
            validate_email(username_or_email)
        except ValidationError:
            is_email = False

        # Lookup user
        try:
            if is_email:
                user = User.objects.get(email=username_or_email)
            else:
                user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return Response({
                "error": "Invalid username/email or password."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify current password
        if not user.check_password(current_password):
            return Response({
                "error": "Invalid username/email or password."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if user is active
        if not user.is_active:
            return Response({
                "error": "User account is inactive."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Prevent reusing the same password
        if current_password == new_password:
            return Response({
                "error": "New password must be different from current password."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Apply new password and flags
            user.set_password(new_password)
            user.must_change_password = False
            user.password_changed_at = timezone.now()
            user.save()

            # Double-check
            user.refresh_from_db()
            if not user.check_password(new_password):
                raise Exception("Password verification failed after save")

            # Log success
            print(f"\n🔐 PASSWORD RESET by user: {user.username}")
            print(f"Email: {user.email}")
            print(f"Reset at: {timezone.now()}")
            print(f"New password verification: ✅")
            print(f"Database save: ✅\n")

            return Response({
                "message": "Password reset successfully.",
                "user": user.username,
                "timestamp": timezone.now(),
                "success": True
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
    
    # @action(detail=False, methods=['get'])
    # def userdata(self, request):
    #     """Get current user's information with admin fields."""
    #     user = request.user
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)


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

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})