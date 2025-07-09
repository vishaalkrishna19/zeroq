# Generated migration to add custom_permissions field to User model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles_permissions', '0001_initial'),
        ('users', '0005_alter_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='custom_permissions',
            field=models.ManyToManyField(
                blank=True, 
                help_text='Additional permissions granted directly to this user', 
                related_name='users_with_permission', 
                to='roles_permissions.permission'
            ),
        ),
    ]