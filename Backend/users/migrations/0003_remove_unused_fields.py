# Generated migration to remove unused fields from User model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_add_direct_account_relationship'),
    ]

    operations = [
        # Remove onboarding/offboarding fields (now handled by UserAccount model)
        migrations.RemoveField(
            model_name='user',
            name='onboarding_completed',
        ),
        migrations.RemoveField(
            model_name='user',
            name='onboarding_completed_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='offboarding_started',
        ),
        migrations.RemoveField(
            model_name='user',
            name='offboarding_started_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='offboarding_completed_at',
        ),
        
        # Remove contact and personal information fields
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        
        # Remove manager field (organizational hierarchy)
        migrations.RemoveField(
            model_name='user',
            name='manager',
        ),
        
        # Remove address fields
        migrations.RemoveField(
            model_name='user',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        
        # Remove security fields not needed
        migrations.RemoveField(
            model_name='user',
            name='last_login_ip',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_system_admin',
        ),
    ]