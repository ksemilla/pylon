# Generated by Django 3.1.12 on 2021-07-25 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='status',
            field=models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], default='a', max_length=64),
        ),
    ]
