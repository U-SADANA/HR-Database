# Generated by Django 4.0 on 2021-12-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_features', '0008_alter_hr_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='hr',
            name='branch',
            field=models.CharField(choices=[('Circuit Branchs', 'Circuit Branchs'), ('Non Circuit Branchs', 'Non Circuit Branchs')], max_length=70, null=True),
        ),
    ]