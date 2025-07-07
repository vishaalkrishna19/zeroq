from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .serializers import LoginSerializer, ChangePasswordSerializer, UserSerializer
from .models import User

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request):
    """API endpoint for user login"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'password_change_required': user.password_change_required
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_api(request):
    """API endpoint for user logout"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    logout(request)
    return Response({'message': 'Successfully logged out'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_api(request):
    """API endpoint for changing password"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.password_changed = True
        user.password_change_required = False
        user.save()
        
        # Update token
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Password changed successfully',
            'token': token.key
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_api(request):
    """Get user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Web Views
def login_view(request):
    """Web login page"""
    if request.user.is_authenticated:
        if request.user.password_change_required:
            return redirect('change_password')
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.password_change_required:
                        return redirect('change_password')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Account is disabled')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Please enter both email and password')
    
    return render(request, 'registration/login.html')

@login_required
def change_password_view(request):
    """Web password change page"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if old_password and new_password and confirm_password:
            if not request.user.check_password(old_password):
                messages.error(request, 'Current password is incorrect')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
            else:
                user = request.user
                user.set_password(new_password)
                user.password_changed = True
                user.password_change_required = False
                user.save()
                
                # Re-authenticate user with new password
                user = authenticate(request, email=user.email, password=new_password)
                if user:
                    login(request, user)
                
                messages.success(request, 'Password changed successfully')
                return redirect('dashboard')
        else:
            messages.error(request, 'Please fill in all fields')
    
    return render(request, 'registration/change_password.html')

@login_required
def dashboard_view(request):
    """Main dashboard"""
    return render(request, 'dashboard/dashboard.html', {'user': request.user})

def logout_view(request):
    """Web logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')
