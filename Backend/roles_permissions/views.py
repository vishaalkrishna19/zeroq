from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import Permission, Role, RolePermission
from .serializers import (
    PermissionSerializer, 
    RoleSerializer, 
    RoleListSerializer,
    AssignPermissionSerializer,
    RolePermissionSerializer
)


class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing permissions.
    Provides CRUD operations for permissions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Permission.objects.all()
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(codename__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by level
        level = self.request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.order_by('category', 'level', 'name')
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all permission categories."""
        categories = Permission.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get permissions grouped by category."""
        permissions = {}
        queryset = self.get_queryset()
        
        for permission in queryset:
            category = permission.category
            if category not in permissions:
                permissions[category] = []
            permissions[category].append(PermissionSerializer(permission).data)
        
        return Response(permissions)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing roles.
    Provides CRUD operations for roles and permission management.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleSerializer
    
    def get_queryset(self):
        queryset = Role.objects.prefetch_related('rolepermission_set__permission')
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(display_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Filter by level
        level = self.request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by system role status
        is_system = self.request.query_params.get('is_system', None)
        if is_system is not None:
            queryset = queryset.filter(is_system_role=is_system.lower() == 'true')
        
        return queryset.order_by('level', 'name')
    
    def destroy(self, request, *args, **kwargs):
        """Prevent deletion of system roles."""
        role = self.get_object()
        if role.is_system_role:
            return Response(
                {"error": "Cannot delete system roles."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """Get all permissions for this role."""
        role = self.get_object()
        role_permissions = role.rolepermission_set.select_related('permission')
        serializer = RolePermissionSerializer(role_permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_permission(self, request, pk=None):
        """Assign a permission to this role."""
        role = self.get_object()
        serializer = AssignPermissionSerializer(data=request.data)
        
        if serializer.is_valid():
            permission_id = serializer.validated_data['permission_id']
            is_granted = serializer.validated_data['is_granted']
            constraints = serializer.validated_data.get('constraints', {})
            
            permission = get_object_or_404(Permission, id=permission_id)
            
            # Create or update role permission
            role_permission, created = RolePermission.objects.update_or_create(
                role=role,
                permission=permission,
                defaults={
                    'is_granted': is_granted,
                    'constraints': constraints,
                    'created_by': request.user
                }
            )
            
            action_text = "assigned" if created else "updated"
            return Response({
                "message": f"Permission {action_text} successfully.",
                "role_permission": RolePermissionSerializer(role_permission).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def remove_permission(self, request, pk=None):
        """Remove a permission from this role."""
        role = self.get_object()
        permission_id = request.query_params.get('permission_id')
        
        if not permission_id:
            return Response(
                {"error": "permission_id is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            role_permission = RolePermission.objects.get(
                role=role, 
                permission_id=permission_id
            )
            role_permission.delete()
            
            return Response({"message": "Permission removed successfully."})
        except RolePermission.DoesNotExist:
            return Response(
                {"error": "Permission not found for this role."}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Get all users with this role."""
        role = self.get_object()
        user_accounts = role.useraccount_set.select_related('user', 'account').filter(
            user__is_active=True
        )
        
        users_data = []
        for ua in user_accounts:
            users_data.append({
                'user_id': ua.user.id,
                'username': ua.user.username,
                'email': ua.user.email,
                'first_name': ua.user.first_name,
                'last_name': ua.user.last_name,
                'account_id': ua.account.id,
                'account_name': ua.account.account_name,
                'assigned_at': ua.created_at
            })
        
        return Response(users_data)
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """Get the default role."""
        try:
            default_role = Role.objects.get(is_default=True, is_active=True)
            serializer = RoleSerializer(default_role)
            return Response(serializer.data)
        except Role.DoesNotExist:
            return Response(
                {"error": "No default role found."}, 
                status=status.HTTP_404_NOT_FOUND
            )