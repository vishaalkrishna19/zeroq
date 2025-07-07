# Generated migration to add account and role fields to User model
# and remove dependency on UserAccount for basic user-company relationship

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('accounts', '0001_initial'),
        ('roles_permissions', '0001_initial'),
    ]

    operations = [
        # Add account field to User model
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.ForeignKey(
                blank=True,
                help_text='Company this user belongs to',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='users',
                to='accounts.account'
            ),
        ),
        # Add role field to User model
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(
                blank=True,
                help_text='User role in the company',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='roles_permissions.role'
            ),
        ),
        # Add onboarding fields to User model
        migrations.AddField(
            model_name='user',
            name='onboarding_completed',
            field=models.BooleanField(
                default=False,
                help_text='Whether onboarding process is completed'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='onboarding_completed_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When onboarding was completed',
                null=True
            ),
        ),
        # Add offboarding fields to User model
        migrations.AddField(
            model_name='user',
            name='offboarding_started',
            field=models.BooleanField(
                default=False,
                help_text='Whether offboarding process has started'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='offboarding_started_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When offboarding was started',
                null=True
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='offboarding_completed_at',
            field=models.DateTimeField(
                blank=True,
                help_text='When offboarding was completed',
                null=True
            ),
        ),
        # Add admin access field to User model
        migrations.AddField(
            model_name='user',
            name='can_access_admin',
            field=models.BooleanField(
                default=False,
                help_text='Whether user can access admin features'
            ),
        ),
    ]