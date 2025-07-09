# Generated migration for adding job_title field to JourneyTemplate

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_merge_0002_add_job_titles_0003_remove_unused_fields'),
        ('boarding', '0001_initial'),
    ]

    operations = [
        # Add job_title field
        migrations.AddField(
            model_name='journeytemplate',
            name='job_title',
            field=models.ForeignKey(
                blank=True,
                help_text='Job title this template applies to',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='journey_templates',
                to='users.jobtitle'
            ),
        ),
        
        # Remove old unique constraint
        migrations.AlterUniqueTogether(
            name='journeytemplate',
            unique_together=set(),
        ),
        
        # Add new unique constraint with job_title
        migrations.AlterUniqueTogether(
            name='journeytemplate',
            unique_together={('account', 'journey_type', 'job_title', 'title')},
        ),
    ]
