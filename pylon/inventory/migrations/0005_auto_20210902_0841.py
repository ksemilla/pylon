# Generated by Django 3.1.12 on 2021-09-02 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20210902_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='location',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='photo',
        ),
    ]
