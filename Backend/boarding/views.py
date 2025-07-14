from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action,api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import JourneyTemplate, JourneyStep, JourneyInstance, JourneyStepInstance
from .serializers import (
    JourneyTemplateSerializer, JourneyTemplateListSerializer, JourneyTemplateCreateSerializer,
    JourneyStepSerializer, JourneyInstanceSerializer, JourneyInstanceListSerializer,
    JourneyInstanceCreateSerializer, JourneyStepInstanceSerializer
)
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_dashboard(request):
    # Total templates by type
    onboarding_templates = JourneyTemplate.objects.filter(journey_type='onboarding').count()
    offboarding_templates = JourneyTemplate.objects.filter(journey_type='offboarding').count()
    
    # Total journeys by type and status
    completed_onboarding = JourneyInstance.objects.filter(
        template__journey_type='onboarding', status='completed'
    ).count()
    completed_offboarding = JourneyInstance.objects.filter(
        template__journey_type='offboarding', status='completed'
    ).count()
    
    # Steps completed for a particular onboarding template (example: template_id from query param)
    template_id = request.query_params.get('template_id')
    steps_completed = None
    if template_id:
        steps_completed = JourneyStepInstance.objects.filter(
            journey__template_id=template_id, status='completed'
        ).count()
    
    return Response({
        "onboarding_template_count": onboarding_templates,
        "offboarding_template_count": offboarding_templates,
        "completed_onboarding_journeys": completed_onboarding,
        "completed_offboarding_journeys": completed_offboarding,
        "steps_completed_for_template": steps_completed,
    })

class JourneyTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing journey templates.
    Provides CRUD operations for onboarding and offboarding templates.
    """
    queryset = JourneyTemplate.objects.all()
    serializer_class = JourneyTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JourneyTemplateListSerializer
        elif self.action == 'create':
            return JourneyTemplateCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return JourneyTemplateCreateSerializer
        return JourneyTemplateSerializer
    
    def get_queryset(self):
        queryset = JourneyTemplate.objects.prefetch_related('steps')
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(department__icontains=search) |
                Q(business_unit__icontains=search)
            )
        
        # Filter by journey type
        journey_type = self.request.query_params.get('journey_type', None)
        if journey_type:
            queryset = queryset.filter(journey_type=journey_type)
        
        # Filter by job title
        # job_title_id = self.request.query_params.get('job_title_id', None)
        # if job_title_id:
        #     queryset = queryset.filter(job_title_id=job_title_id)
        
        # Filter by department
        department = self.request.query_params.get('department', None)
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        # Filter by business unit
        business_unit = self.request.query_params.get('business_unit', None)
        if business_unit:
            queryset = queryset.filter(business_unit__icontains=business_unit)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by account
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        
        return queryset.order_by('journey_type',  'title')
    
    def create(self, request, *args, **kwargs):
        """Override create to set created_by."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        template = serializer.save()
        template.created_by = request.user
        template.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            JourneyTemplateSerializer(template).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        """Get all steps for this template."""
        template = self.get_object()
        steps = template.get_steps_ordered()
        serializer = JourneyStepSerializer(steps, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_step(self, request, pk=None):
        """Add a step to this template."""
        template = self.get_object()
        serializer = JourneyStepSerializer(data=request.data)
        
        if serializer.is_valid():
            step = serializer.save(template=template)
            return Response(JourneyStepSerializer(step).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate this template."""
        template = self.get_object()
        
        # Create new template
        new_template = JourneyTemplate.objects.create(
            journey_type=template.journey_type,
            title=f"{template.title} (Copy)",
            description=template.description,
            department=template.department,
            business_unit=template.business_unit,
            estimated_duration_days=template.estimated_duration_days,
            account=template.account,
            created_by=request.user
        )
        
        # Copy steps
        for step in template.get_steps_ordered():
            JourneyStep.objects.create(
                template=new_template,
                title=step.title,
                description=step.description,
                step_type=step.step_type,
                responsible_party=step.responsible_party,
                responsible_role=step.responsible_role,
                due_days_from_start=step.due_days_from_start,
                estimated_duration_hours=step.estimated_duration_hours,
                order=step.order,
                is_mandatory=step.is_mandatory,
                is_blocking=step.is_blocking,
                requires_approval=step.requires_approval,
                auto_assign=step.auto_assign,
                notes=step.notes
            )
        
        return Response(
            JourneyTemplateSerializer(new_template).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def onboarding(self, request):
        """Get all onboarding templates."""
        templates = self.get_queryset().filter(journey_type='onboarding')
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def offboarding(self, request):
        """Get all offboarding templates."""
        templates = self.get_queryset().filter(journey_type='offboarding')
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def departments(self, request):
        """Get all departments with templates."""
        departments = JourneyTemplate.objects.values_list('department', flat=True).distinct()
        return Response([dept for dept in departments if dept])
    
    @action(detail=False, methods=['get'])
    def business_units(self, request):
        """Get all business units with templates."""
        business_units = JourneyTemplate.objects.values_list('business_unit', flat=True).distinct()
        return Response([unit for unit in business_units if unit])
    
    # @action(detail=False, methods=['get'])
    # def job_titles(self, request):
    #     """Get all job titles with templates."""
    #     from users.models import JobTitle
    #     job_titles = JobTitle.objects.filter(
    #         journey_templates__isnull=False,
    #         is_active=True
    #     ).distinct().values('id', 'title', 'department')
    #     return Response(list(job_titles))
    
    def update(self, request, *args, **kwargs):
        """Override update to handle steps_data."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # The serializer's update method will handle steps_data
        self.perform_update(serializer)
        
        # Return the updated instance with full serializer
        return Response(JourneyTemplateSerializer(instance).data)


class JourneyStepViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing journey steps.
    """
    queryset = JourneyStep.objects.all()
    serializer_class = JourneyStepSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = JourneyStep.objects.select_related('template', 'responsible_party')
        
        # Filter by template
        template_id = self.request.query_params.get('template_id', None)
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        
        # Filter by step type
        step_type = self.request.query_params.get('step_type', None)
        if step_type:
            queryset = queryset.filter(step_type=step_type)
        
        # Filter by responsible party
        responsible_party_id = self.request.query_params.get('responsible_party_id', None)
        if responsible_party_id:
            queryset = queryset.filter(responsible_party_id=responsible_party_id)
        
        return queryset.order_by('template', 'order')


class JourneyInstanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing journey instances.
    """
    queryset = JourneyInstance.objects.all()
    serializer_class = JourneyInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JourneyInstanceListSerializer
        elif self.action == 'create':
            return JourneyInstanceCreateSerializer
        return JourneyInstanceSerializer
    
    def get_queryset(self):
        queryset = JourneyInstance.objects.select_related('template', 'user', 'created_by')
        
        # Filter by user
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by template
        template_id = self.request.query_params.get('template_id', None)
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by journey type
        journey_type = self.request.query_params.get('journey_type', None)
        if journey_type:
            queryset = queryset.filter(template__journey_type=journey_type)
        
        # Filter overdue journeys
        overdue = self.request.query_params.get('overdue', None)
        if overdue is not None:
            from django.utils import timezone
            if overdue.lower() == 'true':
                queryset = queryset.filter(
                    expected_completion_date__lt=timezone.now().date(),
                    status__in=['not_started', 'in_progress']
                )
        
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Override create to set created_by."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        journey = serializer.save()
        journey.created_by = request.user
        journey.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            JourneyInstanceSerializer(journey).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start the journey."""
        journey = self.get_object()
        
        if journey.start_journey(started_by=request.user):
            return Response({
                "message": "Journey started successfully.",
                "journey": JourneyInstanceSerializer(journey).data
            })
        else:
            return Response(
                {"error": "Journey cannot be started."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete the journey."""
        journey = self.get_object()
        
        if journey.complete_journey(completed_by=request.user):
            return Response({
                "message": "Journey completed successfully.",
                "journey": JourneyInstanceSerializer(journey).data
            })
        else:
            return Response(
                {"error": "Journey cannot be completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        """Get all step instances for this journey."""
        journey = self.get_object()
        steps = journey.step_instances.all().order_by('step_template__order')
        serializer = JourneyStepInstanceSerializer(steps, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending journeys."""
        journeys = self.get_queryset().filter(status='not_started')
        serializer = self.get_serializer(journeys, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """Get all in-progress journeys."""
        journeys = self.get_queryset().filter(status='in_progress')
        serializer = self.get_serializer(journeys, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue journeys."""
        from django.utils import timezone
        journeys = self.get_queryset().filter(
            expected_completion_date__lt=timezone.now().date(),
            status__in=['not_started', 'in_progress']
        )
        serializer = self.get_serializer(journeys, many=True)
        return Response(serializer.data)


class JourneyStepInstanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing journey step instances.
    """
    queryset = JourneyStepInstance.objects.all()
    serializer_class = JourneyStepInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = JourneyStepInstance.objects.select_related(
            'journey__user', 'journey__template', 'step_template', 'assigned_to'
        )
        
        # Filter by journey
        journey_id = self.request.query_params.get('journey_id', None)
        if journey_id:
            queryset = queryset.filter(journey_id=journey_id)
        
        # Filter by assigned user
        assigned_to_id = self.request.query_params.get('assigned_to_id', None)
        if assigned_to_id:
            queryset = queryset.filter(assigned_to_id=assigned_to_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter overdue steps
        overdue = self.request.query_params.get('overdue', None)
        if overdue is not None:
            from django.utils import timezone
            if overdue.lower() == 'true':
                queryset = queryset.filter(
                    due_date__lt=timezone.now().date(),
                    status__in=['pending', 'in_progress']
                )
        
        return queryset.order_by('journey', 'step_template__order')
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark step as completed."""
        step = self.get_object()
        notes = request.data.get('completion_notes', '')
        
        if step.mark_completed(completed_by=request.user, notes=notes):
            return Response({
                "message": "Step completed successfully.",
                "step": JourneyStepInstanceSerializer(step).data
            })
        else:
            return Response(
                {"error": "Step cannot be completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get steps assigned to current user."""
        steps = self.get_queryset().filter(
            assigned_to=request.user,
            status__in=['pending', 'in_progress']
        ).order_by('due_date')
        serializer = self.get_serializer(steps, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue steps."""
        from django.utils import timezone
        steps = self.get_queryset().filter(
            due_date__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        )
        serializer = self.get_serializer(steps, many=True)
        return Response(serializer.data)
