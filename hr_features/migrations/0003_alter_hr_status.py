# Generated by Django 3.2.9 on 2021-12-21 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_features', '0002_alter_hr_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hr',
            name='status',
            field=models.CharField(choices=[('Not Called', 'Not Called'), ('Blacklisted Contact', 'Blacklisted Contact'), ('Wrong Number', 'Wrong Number'), ('Called/Not Reachable', 'Called/Not Reachable'), ('Called/Postponed', 'Called/Postponed'), ('Called/Accepted', 'Called/Accepted'), ('Emailed/Awaiting Response', 'Emailed/Awaiting Response'), ('Emailed/Declined', 'Emailed/Declined'), ('Emailed/Confirmed', 'Emailed/Confirmed')], max_length=70),
        ),
    ]
