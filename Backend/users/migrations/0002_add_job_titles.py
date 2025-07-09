# Generated migration for JobTitle model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


def create_default_job_titles(apps, schema_editor):
    """Create default job titles and migrate existing user job titles."""
    JobTitle = apps.get_model('users', 'JobTitle')
    User = apps.get_model('users', 'User')
    
    # Default job titles with boarding template mapping
    default_job_titles = [
        {
            'title': 'Software Engineer',
            'description': 'Develops and maintains software applications',
            'department': 'Engineering',
            'boarding_template_title': 'Technical Onboarding - Engineer'
        },
        {
            'title': 'Senior Software Engineer',
            'description': 'Senior-level software development and mentoring',
            'department': 'Engineering',
            'boarding_template_title': 'Technical Onboarding - Senior Engineer'
        },
        {
            'title': 'Product Manager',
            'description': 'Manages product development and strategy',
            'department': 'Product',
            'boarding_template_title': 'Product Team Onboarding'
        },
        {
            'title': 'Designer',
            'description': 'Creates user interface and experience designs',
            'department': 'Design',
            'boarding_template_title': 'Creative Team Onboarding'
        },
        {
            'title': 'Marketing Manager',
            'description': 'Develops and executes marketing strategies',
            'department': 'Marketing',
            'boarding_template_title': 'Marketing Team Onboarding'
        },
        {
            'title': 'Sales Representative',
            'description': 'Manages client relationships and sales',
            'department': 'Sales',
            'boarding_template_title': 'Sales Team Onboarding'
        },
        {
            'title': 'HR Manager',
            'description': 'Manages human resources and employee relations',
            'department': 'HR',
            'boarding_template_title': 'HR Team Onboarding'
        },
        {
            'title': 'System Administrator',
            'description': 'Manages IT infrastructure and systems',
            'department': 'IT',
            'boarding_template_title': 'IT Infrastructure Onboarding'
        },
    ]
    
    # Create job titles
    created_job_titles = {}
    for job_data in default_job_titles:
        job_title, created = JobTitle.objects.get_or_create(
            title=job_data['title'],
            defaults={
                'description': job_data['description'],
                'department': job_data['department'],
                'boarding_template_title': job_data['boarding_template_title'],
                'is_active': True
            }
        )
        created_job_titles[job_data['title']] = job_title
    
    # Migrate existing user job titles
    for user in User.objects.all():
        if user.job_title_old:  # This will be the old CharField value
            # Try to match existing job title or create new one
            job_title = created_job_titles.get(user.job_title_old)
            if not job_title:
                # Create custom job title for existing data
                job_title, created = JobTitle.objects.get_or_create(
                    title=user.job_title_old,
                    defaults={
                        'description': f'Migrated job title: {user.job_title_old}',
                        'department': user.department or 'General',
                        'boarding_template_title': f'General Onboarding - {user.job_title_old}',
                        'is_active': True
                    }
                )
            user.job_title_new = job_title
            user.save()


def reverse_job_titles(apps, schema_editor):
    """Reverse migration - copy job title names back to CharField."""
    User = apps.get_model('users', 'User')
    
    for user in User.objects.all():
        if user.job_title_new:
            user.job_title_old = user.job_title_new.title
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # Create JobTitle model
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Job title name', max_length=100, unique=True)),
                ('description', models.TextField(blank=True, help_text='Description of the job title and responsibilities')),
                ('department', models.CharField(blank=True, help_text='Primary department for this job title', max_length=100)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this job title is available for selection')),
                ('boarding_template_title', models.CharField(blank=True, help_text='Corresponding boarding template title for onboarding', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this job title', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_job_titles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Title',
                'verbose_name_plural': 'Job Titles',
                'db_table': 'job_titles',
                'ordering': ['title'],
            },
        ),
        
        # Rename old job_title field
        migrations.RenameField(
            model_name='user',
            old_name='job_title',
            new_name='job_title_old',
        ),
        
        # Add new job_title ForeignKey field
        migrations.AddField(
            model_name='user',
            name='job_title_new',
            field=models.ForeignKey(blank=True, help_text='Current job title', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='users.jobtitle'),
        ),
        
        # Migrate data
        migrations.RunPython(create_default_job_titles, reverse_job_titles),
        
        # Remove old field and rename new field
        migrations.RemoveField(
            model_name='user',
            name='job_title_old',
        ),
        
        migrations.RenameField(
            model_name='user',
            old_name='job_title_new',
            new_name='job_title',
        ),
    ]
