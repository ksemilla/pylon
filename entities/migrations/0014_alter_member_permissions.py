# Generated by Django 5.1.4 on 2025-01-22 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0013_member_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='permissions',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
