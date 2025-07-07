from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Account
from .serializers import AccountSerializer, AccountListSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing company accounts.
    Provides CRUD operations for accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListSerializer
        return AccountSerializer
    
    def get_queryset(self):
        queryset = Account.objects.all()
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(account_name__icontains=search) |
                Q(account_id__icontains=search) |
                Q(contact_email__icontains=search)
            )
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by subscription type
        subscription_type = self.request.query_params.get('subscription_type', None)
        if subscription_type:
            queryset = queryset.filter(subscription_type=subscription_type)
        
        return queryset.order_by('account_name')
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """Get all users for this account."""
        account = self.get_object()
        users = account.get_active_users()
        
        from users.serializers import UserListSerializer
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def admins(self, request, pk=None):
        """Get all admin users for this account."""
        account = self.get_object()
        admins = account.get_admin_users()
        
        from users.serializers import UserListSerializer
        serializer = UserListSerializer(admins, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate an account."""
        account = self.get_object()
        account.is_active = False
        account.save()
        
        serializer = self.get_serializer(account)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate an account."""
        account = self.get_object()
        account.is_active = True
        account.save()
        
        serializer = self.get_serializer(account)
        return Response(serializer.data)