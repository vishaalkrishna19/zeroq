from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class JourneyTemplate(models.Model):
    """
    Template for onboarding/offboarding journeys.
    Defines the steps and process for specific job titles or departments.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Journey type
    JOURNEY_TYPE_CHOICES = [
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding'),
    ]
    
    journey_type = models.CharField(
        max_length=20,
        choices=JOURNEY_TYPE_CHOICES,
        default='onboarding',
        help_text='Type of journey this template represents'
    )
    
    # Journey details
    title = models.CharField(
        max_length=200,
        help_text='Display title for this journey template'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Brief description of the boarding process'
    )
    
    # Job title relationship
    job_title = models.ForeignKey(
        'users.JobTitle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='journey_templates',
        help_text='Job title this template applies to'
    )
    
    # Organizational details
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Department this template applies to (auto-filled from job title)'
    )
    
    business_unit = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Business unit this template applies to'
    )
    
    # Duration
    estimated_duration_days = models.PositiveIntegerField(
        help_text='Estimated duration in days for completing this journey'
    )
    
    # Account relationship
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='journey_templates',
        help_text='Account this template belongs to'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this template is currently active'
    )
    
    is_default = models.BooleanField(
        default=False,
        help_text='Whether this is the default template for the department/type'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_journey_templates',
        help_text='User who created this template'
    )
    
    class Meta:
        db_table = 'journey_templates'
        verbose_name = 'Journey Template'
        verbose_name_plural = 'Journey Templates'
        ordering = ['journey_type', 'department', 'title']
        unique_together = ['account', 'journey_type', 'title']
        
    def __str__(self):
        return f"{self.get_journey_type_display()}: {self.title}"
    
    def clean(self):
        # Auto-fill department from job title if available
        if self.job_title and not self.department:
            self.department = self.job_title.department
            
        # Ensure only one default template per account/journey_type/job_title
        if self.is_default:
            existing_default = JourneyTemplate.objects.filter(
                account=self.account,
                journey_type=self.journey_type,
                job_title=self.job_title,
                is_default=True
            ).exclude(pk=self.pk)
            
            if existing_default.exists():
                job_title_str = f" for {self.job_title.title}" if self.job_title else ""
                raise ValidationError(
                    f'A default {self.journey_type} template already exists{job_title_str}.'
                )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def step_count(self):
        """Return the number of steps in this template."""
        return self.steps.count()
    
    def get_steps_ordered(self):
        """Get steps ordered by their order field."""
        return self.steps.all().order_by('order', 'due_days_from_start')


class JourneyStep(models.Model):
    """
    Individual step within a journey template.
    Defines specific tasks and requirements for the boarding process.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationship to template
    template = models.ForeignKey(
        JourneyTemplate,
        on_delete=models.CASCADE,
        related_name='steps',
        help_text='Journey template this step belongs to'
    )
    
    # Step details
    title = models.CharField(
        max_length=200,
        help_text='Title of the step (e.g., Complete HR Orientation)'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Detailed instructions for this step'
    )
    
    # Step type
    STEP_TYPE_CHOICES = [
        ('orientation', 'Orientation'),
        ('documentation', 'Documentation'),
        ('training', 'Training'),
        ('system_access', 'System Access'),
        ('equipment', 'Equipment Setup'),
        ('meeting', 'Meeting/Interview'),
        ('review', 'Review/Approval'),
        ('handover', 'Handover'),
        ('exit_interview', 'Exit Interview'),
        ('asset_return', 'Asset Return'),
        ('access_revocation', 'Access Revocation'),
        ('final_settlement', 'Final Settlement'),
        ('other', 'Other'),
    ]
    
    step_type = models.CharField(
        max_length=50,
        choices=STEP_TYPE_CHOICES,
        help_text='Category/type of this step'
    )
    
    # Responsibility
    responsible_party = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_journey_steps',
        help_text='User responsible for completing this step'
    )
    
    responsible_role = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Role responsible for this step (e.g., HR, IT Admin, Manager)'
    )
    
    # Timing
    due_days_from_start = models.PositiveIntegerField(
        help_text='Number of days from journey start when this step is due'
    )
    
    estimated_duration_hours = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Estimated time to complete this step (in hours)'
    )
    
    # Step order and dependencies
    order = models.PositiveIntegerField(
        default=1,
        help_text='Order of this step in the journey'
    )
    
    is_mandatory = models.BooleanField(
        default=True,
        help_text='Whether this step is mandatory for journey completion'
    )
    
    is_blocking = models.BooleanField(
        default=False,
        help_text='Whether subsequent steps cannot start until this is completed'
    )
    
    # Additional settings
    requires_approval = models.BooleanField(
        default=False,
        help_text='Whether this step requires approval to mark as complete'
    )
    
    auto_assign = models.BooleanField(
        default=True,
        help_text='Whether this step should be auto-assigned when journey starts'
    )
    
    # Notes and attachments
    notes = models.TextField(
        blank=True,
        help_text='Additional notes or requirements for this step'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this step is currently active'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'journey_steps'
        verbose_name = 'Journey Step'
        verbose_name_plural = 'Journey Steps'
        ordering = ['template', 'order', 'due_days_from_start']
        unique_together = ['template', 'order']
        
    def __str__(self):
        return f"{self.template.title} - Step {self.order}: {self.title}"
    
    def clean(self):
        # Validate due_days_from_start doesn't exceed template duration
        if (self.template and 
            self.due_days_from_start > self.template.estimated_duration_days):
            raise ValidationError(
                f'Due date ({self.due_days_from_start} days) cannot exceed '
                f'template duration ({self.template.estimated_duration_days} days)'
            )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def responsible_display(self):
        """Return a display-friendly responsible party."""
        if self.responsible_party:
            return self.responsible_party.get_full_name()
        elif self.responsible_role:
            return self.responsible_role
        else:
            return "Unassigned"


class JourneyInstance(models.Model):
    """
    Actual journey instance created from a template for a specific user.
    Tracks the progress of an individual's boarding process.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    template = models.ForeignKey(
        JourneyTemplate,
        on_delete=models.PROTECT,
        related_name='instances',
        help_text='Template this journey is based on'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='journey_instances',
        help_text='User undergoing this journey'
    )
    
    # Journey status
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started',
        help_text='Current status of this journey'
    )
    
    # Dates
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date when the journey started'
    )
    
    expected_completion_date = models.DateField(
        null=True,
        blank=True,
        help_text='Expected completion date based on template duration'
    )
    
    actual_completion_date = models.DateField(
        null=True,
        blank=True,
        help_text='Actual completion date'
    )
    
    # Progress tracking
    total_steps = models.PositiveIntegerField(
        default=0,
        help_text='Total number of steps in this journey'
    )
    
    completed_steps = models.PositiveIntegerField(
        default=0,
        help_text='Number of completed steps'
    )
    
    # Notes and metadata
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about this journey instance'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_journey_instances',
        help_text='User who created this journey instance'
    )
    
    class Meta:
        db_table = 'journey_instances'
        verbose_name = 'Journey Instance'
        verbose_name_plural = 'Journey Instances'
        ordering = ['-created_at']
        unique_together = ['template', 'user']
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.template.title}"
    
    @property
    def progress_percentage(self):
        """Calculate completion percentage."""
        if self.total_steps == 0:
            return 0
        return round((self.completed_steps / self.total_steps) * 100, 1)
    
    @property
    def is_overdue(self):
        """Check if journey is overdue."""
        if not self.expected_completion_date or self.status == 'completed':
            return False
        
        from django.utils import timezone
        return timezone.now().date() > self.expected_completion_date
    
    def start_journey(self, started_by=None):
        """Start the journey and create step instances."""
        if self.status != 'not_started':
            return False
        
        from django.utils import timezone
        from datetime import timedelta
        
        self.status = 'in_progress'
        self.start_date = timezone.now().date()
        self.expected_completion_date = self.start_date + timedelta(
            days=self.template.estimated_duration_days
        )
        self.total_steps = self.template.step_count
        self.save()
        
        # Create step instances
        for step in self.template.get_steps_ordered():
            JourneyStepInstance.objects.create(
                journey=self,
                step_template=step,
                due_date=self.start_date + timedelta(days=step.due_days_from_start),
                assigned_to=step.responsible_party,
                created_by=started_by
            )
        
        return True
    
    def complete_journey(self, completed_by=None):
        """Mark journey as completed."""
        if self.status not in ['in_progress', 'on_hold']:
            return False
        
        from django.utils import timezone
        
        self.status = 'completed'
        self.actual_completion_date = timezone.now().date()
        self.completed_steps = self.total_steps
        self.save()
        
        return True


class JourneyStepInstance(models.Model):
    """
    Individual step instance for a specific journey.
    Tracks the completion status of each step.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    journey = models.ForeignKey(
        JourneyInstance,
        on_delete=models.CASCADE,
        related_name='step_instances',
        help_text='Journey this step belongs to'
    )
    
    step_template = models.ForeignKey(
        JourneyStep,
        on_delete=models.PROTECT,
        related_name='instances',
        help_text='Template step this instance is based on'
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_step_instances',
        help_text='User assigned to complete this step'
    )
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
        ('blocked', 'Blocked'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Current status of this step'
    )
    
    # Dates
    due_date = models.DateField(
        help_text='Date when this step is due'
    )
    
    started_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When work on this step was started'
    )
    
    completed_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When this step was completed'
    )
    
    # Completion details
    completion_notes = models.TextField(
        blank=True,
        help_text='Notes about step completion'
    )
    
    completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_step_instances',
        help_text='User who marked this step as completed'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_step_instances',
        help_text='User who created this step instance'
    )
    
    class Meta:
        db_table = 'journey_step_instances'
        verbose_name = 'Journey Step Instance'
        verbose_name_plural = 'Journey Step Instances'
        ordering = ['journey', 'step_template__order']
        
    def __str__(self):
        return f"{self.journey.user.get_full_name()} - {self.step_template.title}"
    
    @property
    def is_overdue(self):
        """Check if step is overdue."""
        if self.status == 'completed':
            return False
        
        from django.utils import timezone
        return timezone.now().date() > self.due_date
    
    def mark_completed(self, completed_by=None, notes=""):
        """Mark step as completed."""
        if self.status == 'completed':
            return False
        
        from django.utils import timezone
        
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.completed_by = completed_by
        self.completion_notes = notes
        self.save()
        
        # Update journey progress
        self.journey.completed_steps = self.journey.step_instances.filter(
            status='completed'
        ).count()
        self.journey.save()
        
        # Check if journey is complete
        if self.journey.completed_steps >= self.journey.total_steps:
            self.journey.complete_journey(completed_by)
            return True
