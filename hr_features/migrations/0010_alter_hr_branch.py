# Generated by Django 4.0 on 2021-12-31 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_features', '0009_hr_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hr',
            name='branch',
            field=models.CharField(choices=[('Circuit Branches', 'Circuit Branches'), ('Non Circuit Branches', 'Non Circuit Branches')], max_length=70, null=True),
        ),
    ]
