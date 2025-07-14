from rest_framework import serializers
from .models import JourneyTemplate, JourneyStep, JourneyInstance, JourneyStepInstance


class JourneyStepSerializer(serializers.ModelSerializer):
    responsible_display = serializers.ReadOnlyField()
    
    class Meta:
        model = JourneyStep
        fields = [
            'id', 'title', 'description', 'step_type', 'responsible_party',
            'responsible_role', 'responsible_display', 'due_days_from_start',
            'estimated_duration_hours', 'order', 'is_mandatory', 'is_blocking',
            'requires_approval', 'auto_assign', 'notes', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class JourneyStepCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyStep
        fields = [
            'title', 'description', 'step_type', 'responsible_party',
            'responsible_role', 'due_days_from_start', 'estimated_duration_hours',
            'order', 'is_mandatory', 'is_blocking', 'requires_approval',
            'auto_assign', 'notes', 'is_active'
        ]


class JourneyTemplateSerializer(serializers.ModelSerializer):
    steps = JourneyStepSerializer(many=True, read_only=True)
    step_count = serializers.ReadOnlyField()
    # job_title_name = serializers.CharField(source='job_title.title', read_only=True)
    user_count = serializers.SerializerMethodField()  # <-- FIXED

    class Meta:
        model = JourneyTemplate
        fields = [
            'id', 'journey_type', 'title', 'description', 
            'department', 'business_unit', 'estimated_duration_days', 'account',
            'is_active', 'is_default', 'step_count', 'steps','user_count',
            
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    def get_step_count(self, obj):
        return obj.steps.count()

    def get_user_count(self, obj):
        # Assumes User model has a ForeignKey to JourneyTemplate as 'template'
        return obj.assigned_users.count()

    

class JourneyTemplateListSerializer(serializers.ModelSerializer):
    step_count = serializers.ReadOnlyField()
    account_name = serializers.CharField(source='account.account_name', read_only=True)
    user_count = serializers.SerializerMethodField()  # <-- FIXED
    
    class Meta:
        model = JourneyTemplate
        fields = [
            'id', 'journey_type', 'title',  'department', 'business_unit',
            'estimated_duration_days', 'account_name', 'is_active',
            'is_default', 'step_count', 'created_at', 'user_count'
        ]
    def get_user_count(self, obj):
        # Assumes User model has a ForeignKey to JourneyTemplate as 'template'
        return obj.assigned_users.count()

class JourneyTemplateCreateSerializer(serializers.ModelSerializer):
    steps_data = JourneyStepCreateSerializer(many=True, write_only=True, required=False)
    
    class Meta:
        model = JourneyTemplate
        fields = [
            'journey_type', 'title', 'description',  'department',
            'business_unit', 'estimated_duration_days', 'account',
            'is_active', 'is_default', 'steps_data'
        ]
    
    # def validate_job_title(self, value):
    #     """Ensure job title is active."""
    #     if value and not value.is_active:
    #         raise serializers.ValidationError("Selected job title is not active.")
    #     return value
    
    def validate(self, data):
        """Custom validation for unique constraints during update."""
        if self.instance:  # This is an update
            # Check for unique constraint violations
            existing_template = JourneyTemplate.objects.filter(
                account=data.get('account', self.instance.account),
                journey_type=data.get('journey_type', self.instance.journey_type),
                
                title=data.get('title', self.instance.title)
            ).exclude(pk=self.instance.pk)
            
            if existing_template.exists():
                raise serializers.ValidationError(
                    "A template with this combination already exists."
                )
        
        return data
    
    def create(self, validated_data):
        steps_data = validated_data.pop('steps_data', [])
        template = JourneyTemplate.objects.create(**validated_data)
        
        # Create steps
        for step_data in steps_data:
            JourneyStep.objects.create(template=template, **step_data)
        
        return template
    
    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps_data', None)
        
        # Update template fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update steps if provided
        if steps_data is not None:
            # Delete existing steps
            instance.steps.all().delete()
            
            # Create new steps
            for step_data in steps_data:
                JourneyStep.objects.create(template=instance, **step_data)
        
        return instance


class JourneyStepInstanceSerializer(serializers.ModelSerializer):
    step_title = serializers.CharField(source='step_template.title', read_only=True)
    step_type = serializers.CharField(source='step_template.step_type', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    completed_by_name = serializers.CharField(source='completed_by.get_full_name', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = JourneyStepInstance
        fields = [
            'id', 'step_template', 'step_title', 'step_type', 'assigned_to',
            'assigned_to_name', 'status', 'due_date', 'started_date',
            'completed_date', 'completion_notes', 'completed_by',
            'completed_by_name', 'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class JourneyInstanceSerializer(serializers.ModelSerializer):
    step_instances = JourneyStepInstanceSerializer(many=True, read_only=True)
    template_title = serializers.CharField(source='template.title', read_only=True)
    template_type = serializers.CharField(source='template.journey_type', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = JourneyInstance
        fields = [
            'id', 'template', 'template_title', 'template_type', 'user',
            'user_name', 'status', 'start_date', 'expected_completion_date',
            'actual_completion_date', 'total_steps', 'completed_steps',
            'progress_percentage', 'is_overdue', 'notes', 'step_instances',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class JourneyInstanceListSerializer(serializers.ModelSerializer):
    template_title = serializers.CharField(source='template.title', read_only=True)
    template_type = serializers.CharField(source='template.journey_type', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = JourneyInstance
        fields = [
            'id', 'template_title', 'template_type', 'user_name', 'status',
            'start_date', 'expected_completion_date', 'progress_percentage',
            'is_overdue', 'created_at'
        ]


class JourneyInstanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyInstance
        fields = ['template', 'user', 'notes']
    
    def validate(self, data):
        # Check if journey already exists for this user and template
        if JourneyInstance.objects.filter(
            template=data['template'],
            user=data['user']
        ).exists():
            raise serializers.ValidationError(
                "Journey already exists for this user and template."
            )
        return data
