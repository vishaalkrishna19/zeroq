from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_save, sender='boarding.JourneyTemplate')
def journey_template_created(sender, instance, created, **kwargs):
    """Handle actions when a journey template is created."""
    if created:
        print(f"✅ Journey Template created: {instance.title} ({instance.journey_type})")


@receiver(post_save, sender='boarding.JourneyInstance')
def journey_instance_created(sender, instance, created, **kwargs):
    """Handle actions when a journey instance is created."""
    if created:
        print(f"✅ Journey Instance created: {instance.user.get_full_name()} - {instance.template.title}")


@receiver(post_migrate)
def create_default_journey_templates(sender, **kwargs):
    """Create default journey templates after migration."""
    if sender.name != 'boarding':
        return
    
    JourneyTemplate = apps.get_model('boarding', 'JourneyTemplate')
    JourneyStep = apps.get_model('boarding', 'JourneyStep')
    Account = apps.get_model('accounts', 'Account')
    JobTitle = apps.get_model('users', 'JobTitle')
    
    # Only create if no templates exist
    if JourneyTemplate.objects.exists():
        return
    
    # Get or create a default account for templates
    try:
        default_account = Account.objects.first()
        if not default_account:
            print("⚠️ No accounts found. Skipping default template creation.")
            return
        
        # Get Software Engineer job title
        try:
            software_engineer_job = JobTitle.objects.get(title='Software Engineer')
        except JobTitle.DoesNotExist:
            software_engineer_job = None
            print("⚠️ Software Engineer job title not found. Creating template without job title.")
        
        # Create default onboarding template
        onboarding_template = JourneyTemplate.objects.create(
            journey_type='onboarding',
            title='Software Engineer Onboarding',
            description='Standard onboarding process for software engineers',
            job_title=software_engineer_job,
            department='Engineering',
            business_unit='Technology',
            estimated_duration_days=14,
            account=default_account,
            is_default=True
        )
        
        # Create default onboarding steps
        onboarding_steps = [
            {
                'title': 'Complete HR Orientation',
                'description': 'Attend HR orientation session and complete required paperwork',
                'step_type': 'orientation',
                'responsible_role': 'HR Manager',
                'due_days_from_start': 1,
                'order': 1,
                'is_mandatory': True
            },
            {
                'title': 'IT Setup and System Access',
                'description': 'Get laptop, accounts, and system access configured',
                'step_type': 'system_access',
                'responsible_role': 'IT Administrator',
                'due_days_from_start': 2,
                'order': 2,
                'is_mandatory': True
            },
            {
                'title': 'Team Introduction Meeting',
                'description': 'Meet your team members and understand team structure',
                'step_type': 'meeting',
                'responsible_role': 'Direct Manager',
                'due_days_from_start': 3,
                'order': 3,
                'is_mandatory': True
            },
            {
                'title': 'Code Repository Access',
                'description': 'Get access to code repositories and development tools',
                'step_type': 'system_access',
                'responsible_role': 'Tech Lead',
                'due_days_from_start': 5,
                'order': 4,
                'is_mandatory': True
            },
            {
                'title': '30-Day Review',
                'description': 'Performance review and feedback session',
                'step_type': 'review',
                'responsible_role': 'Direct Manager',
                'due_days_from_start': 14,
                'order': 5,
                'is_mandatory': True
            }
        ]
        
        for step_data in onboarding_steps:
            JourneyStep.objects.create(template=onboarding_template, **step_data)
        
        # Create default offboarding template
        offboarding_template = JourneyTemplate.objects.create(
            journey_type='offboarding',
            title='Software Engineer Offboarding',
            description='Standard offboarding process for software engineers',
            job_title=software_engineer_job,
            department='Engineering',
            business_unit='Technology',
            estimated_duration_days=7,
            account=default_account,
            is_default=True
        )
        
        # Create default offboarding steps
        offboarding_steps = [
            {
                'title': 'Knowledge Transfer Session',
                'description': 'Document and transfer ongoing projects and responsibilities',
                'step_type': 'handover',
                'responsible_role': 'Direct Manager',
                'due_days_from_start': 1,
                'order': 1,
                'is_mandatory': True
            },
            {
                'title': 'Return Company Assets',
                'description': 'Return laptop, access cards, and other company property',
                'step_type': 'asset_return',
                'responsible_role': 'IT Administrator',
                'due_days_from_start': 3,
                'order': 2,
                'is_mandatory': True
            },
            {
                'title': 'Revoke System Access',
                'description': 'Disable all system accounts and access permissions',
                'step_type': 'access_revocation',
                'responsible_role': 'IT Administrator',
                'due_days_from_start': 5,
                'order': 3,
                'is_mandatory': True
            },
            {
                'title': 'Exit Interview',
                'description': 'Conduct exit interview and collect feedback',
                'step_type': 'exit_interview',
                'responsible_role': 'HR Manager',
                'due_days_from_start': 6,
                'order': 4,
                'is_mandatory': True
            },
            {
                'title': 'Final Settlement',
                'description': 'Process final payroll and benefits settlement',
                'step_type': 'final_settlement',
                'responsible_role': 'HR Manager',
                'due_days_from_start': 7,
                'order': 5,
                'is_mandatory': True
            }
        ]
        
        for step_data in offboarding_steps:
            JourneyStep.objects.create(template=offboarding_template, **step_data)
        
        print(f"✅ Created default onboarding template: {onboarding_template.title}")
        print(f"✅ Created default offboarding template: {offboarding_template.title}")
        
    except Exception as e:
        print(f"❌ Error creating default templates: {e}")