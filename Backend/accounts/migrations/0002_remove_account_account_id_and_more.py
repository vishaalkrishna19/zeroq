# Generated by Django 4.2.23 on 2025-07-10 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='account',
            name='subscription_type',
        ),
    ]
