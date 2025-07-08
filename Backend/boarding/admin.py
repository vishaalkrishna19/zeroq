from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import JourneyTemplate, JourneyStep, JourneyInstance, JourneyStepInstance


class JourneyStepInline(admin.TabularInline):
    model = JourneyStep
    extra = 1
    fields = [
        'order', 'title', 'step_type', 'responsible_party', 
        'due_days_from_start', 'is_mandatory', 'is_blocking'
    ]
    ordering = ['order']


@admin.register(JourneyTemplate)
class JourneyTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'journey_type',
        'job_title_display',
        'department',
        'business_unit',
        'estimated_duration_days',
        'step_count_display',
        'is_default',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'journey_type',
        'job_title',
        'department',
        'business_unit',
        'is_active',
        'is_default',
        'account',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'description',
        'job_title__title',
        'department',
        'business_unit'
    ]
    
    readonly_fields = [
        'id',
        'step_count_display',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Journey Type Selection', {
            'fields': ('journey_type',),
            'description': 'Select whether this is an onboarding or offboarding template.'
        }),
        ('Journey Details', {
            'fields': (
                'title',
                'description',
                'estimated_duration_days'
            )
        }),
        ('Organization', {
            'fields': (
                'account',
                'job_title',
                'department',
                'business_unit'
            ),
            'description': 'Select job title first - department will auto-populate if available.'
        }),
        ('Settings', {
            'fields': (
                'is_active',
                'is_default'
            )
        }),
        ('Metadata', {
            'fields': (
                'id',
                'step_count_display',
                'created_by',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [JourneyStepInline]
    ordering = ['journey_type', 'department', 'title']
    
    def step_count_display(self, obj):
        count = obj.step_count
        return format_html(
            '<span style="color: {};">{} steps</span>',
            'green' if count > 0 else 'orange',
            count
        )
    step_count_display.short_description = 'Steps'
    
    def save_model(self, request, obj, form, change):
        """Override to set created_by for new objects."""
        try:
            if not change:
                obj.created_by = request.user
            
            super().save_model(request, obj, form, change)
            obj.refresh_from_db()
            
            action = "created" if not change else "updated"
            print(f"✅ Journey Template {action}: {obj.title} ({obj.journey_type})")
            
        except Exception as e:
            print(f"❌ Error saving Journey Template: {e}")
            raise
    
    def job_title_display(self, obj):
        if obj.job_title:
            return obj.job_title.title
        return "No Job Title"
    job_title_display.short_description = 'Job Title'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('account', 'created_by', 'job_title')


@admin.register(JourneyStep)
class JourneyStepAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'template_display',
        'step_type',
        'order',
        'due_days_from_start',
        'responsible_display',
        'is_mandatory',
        'is_active'
    ]
    
    list_filter = [
        'step_type',
        'is_mandatory',
        'is_blocking',
        'is_active',
        'template__journey_type',
        'template__department'
    ]
    
    search_fields = [
        'title',
        'description',
        'template__title',
        'responsible_role'
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Step Details', {
            'fields': (
                'template',
                'title',
                'description',
                'step_type'
            )
        }),
        ('Responsibility', {
            'fields': (
                'responsible_party',
                'responsible_role'
            )
        }),
        ('Timing & Order', {
            'fields': (
                'order',
                'due_days_from_start',
                'estimated_duration_hours'
            )
        }),
        ('Requirements', {
            'fields': (
                'is_mandatory',
                'is_blocking',
                'requires_approval',
                'auto_assign'
            )
        }),
        ('Additional Information', {
            'fields': (
                'notes',
                'is_active'
            )
        }),
        ('Metadata', {
            'fields': (
                'id',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['template', 'order']
    
    def template_display(self, obj):
        return f"{obj.template.title} ({obj.template.get_journey_type_display()})"
    template_display.short_description = 'Template'
    
    def responsible_display(self, obj):
        return obj.responsible_display
    responsible_display.short_description = 'Responsible'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'template', 'responsible_party'
        )


class JourneyStepInstanceInline(admin.TabularInline):
    model = JourneyStepInstance
    extra = 0
    fields = [
        'step_template', 'assigned_to', 'status', 'due_date', 
        'completed_date', 'completion_notes'
    ]
    readonly_fields = ['step_template', 'due_date']


@admin.register(JourneyInstance)
class JourneyInstanceAdmin(admin.ModelAdmin):
    list_display = [
        'user_display',
        'template_display',
        'status',
        'progress_display',
        'start_date',
        'expected_completion_date',
        'is_overdue_display',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'template__journey_type',
        'template__department',
        'start_date',
        'expected_completion_date'
    ]
    
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'template__title'
    ]
    
    readonly_fields = [
        'id',
        'progress_display',
        'is_overdue_display',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Journey Information', {
            'fields': (
                'template',
                'user',
                'status'
            )
        }),
        ('Timeline', {
            'fields': (
                'start_date',
                'expected_completion_date',
                'actual_completion_date'
            )
        }),
        ('Progress', {
            'fields': (
                'total_steps',
                'completed_steps',
                'progress_display',
                'is_overdue_display'
            )
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': (
                'id',
                'created_by',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [JourneyStepInstanceInline]
    ordering = ['-created_at']
    
    actions = ['start_selected_journeys', 'complete_selected_journeys']
    
    def user_display(self, obj):
        return obj.user.get_full_name()
    user_display.short_description = 'User'
    
    def template_display(self, obj):
        return f"{obj.template.title} ({obj.template.get_journey_type_display()})"
    template_display.short_description = 'Template'
    
    def progress_display(self, obj):
        percentage = obj.progress_percentage
        color = 'green' if percentage == 100 else 'orange' if percentage > 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}% ({}/{})</span>',
            color,
            percentage,
            obj.completed_steps,
            obj.total_steps
        )
    progress_display.short_description = 'Progress'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ Overdue</span>')
        return format_html('<span style="color: green;">✓ On Track</span>')
    is_overdue_display.short_description = 'Status'
    
    def start_selected_journeys(self, request, queryset):
        """Admin action to start selected journeys."""
        started_count = 0
        for journey in queryset.filter(status='not_started'):
            if journey.start_journey(started_by=request.user):
                started_count += 1
        
        self.message_user(request, f"Started {started_count} journeys.")
    start_selected_journeys.short_description = "Start selected journeys"
    
    def complete_selected_journeys(self, request, queryset):
        """Admin action to complete selected journeys."""
        completed_count = 0
        for journey in queryset.filter(status='in_progress'):
            if journey.complete_journey(completed_by=request.user):
                completed_count += 1
        
        self.message_user(request, f"Completed {completed_count} journeys.")
    complete_selected_journeys.short_description = "Complete selected journeys"
    
    def save_model(self, request, obj, form, change):
        """Override to set created_by for new objects."""
        try:
            if not change:
                obj.created_by = request.user
            
            super().save_model(request, obj, form, change)
            obj.refresh_from_db()
            
            action = "created" if not change else "updated"
            print(f"✅ Journey Instance {action}: {obj.user.get_full_name()} - {obj.template.title}")
            
        except Exception as e:
            print(f"❌ Error saving Journey Instance: {e}")
            raise
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'template', 'created_by'
        )


@admin.register(JourneyStepInstance)
class JourneyStepInstanceAdmin(admin.ModelAdmin):
    list_display = [
        'step_title',
        'journey_display',
        'assigned_to',
        'status',
        'due_date',
        'is_overdue_display',
        'completed_date'
    ]
    
    list_filter = [
        'status',
        'step_template__step_type',
        'due_date',
        'completed_date'
    ]
    
    search_fields = [
        'step_template__title',
        'journey__user__username',
        'journey__user__first_name',
        'journey__user__last_name',
        'assigned_to__username'
    ]
    
    readonly_fields = [
        'id',
        'is_overdue_display',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Step Information', {
            'fields': (
                'journey',
                'step_template',
                'assigned_to',
                'status'
            )
        }),
        ('Timeline', {
            'fields': (
                'due_date',
                'started_date',
                'completed_date',
                'is_overdue_display'
            )
        }),
        ('Completion', {
            'fields': (
                'completion_notes',
                'completed_by'
            )
        }),
        ('Metadata', {
            'fields': (
                'id',
                'created_by',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['journey', 'step_template__order']
    
    actions = ['mark_completed', 'mark_in_progress']
    
    def step_title(self, obj):
        return obj.step_template.title
    step_title.short_description = 'Step'
    
    def journey_display(self, obj):
        return f"{obj.journey.user.get_full_name()} - {obj.journey.template.title}"
    journey_display.short_description = 'Journey'
    
    def is_overdue_display(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ Overdue</span>')
        return format_html('<span style="color: green;">✓ On Time</span>')
    is_overdue_display.short_description = 'Due Status'
    
    def mark_completed(self, request, queryset):
        """Admin action to mark selected steps as completed."""
        completed_count = 0
        for step in queryset.exclude(status='completed'):
            if step.mark_completed(completed_by=request.user):
                completed_count += 1
        
        self.message_user(request, f"Marked {completed_count} steps as completed.")
    mark_completed.short_description = "Mark selected steps as completed"
    
    def mark_in_progress(self, request, queryset):
        """Admin action to mark selected steps as in progress."""
        updated = queryset.filter(status='pending').update(status='in_progress')
        self.message_user(request, f"Marked {updated} steps as in progress.")
    mark_in_progress.short_description = "Mark selected steps as in progress"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'journey__user', 'journey__template', 'step_template', 
            'assigned_to', 'completed_by'
        )
