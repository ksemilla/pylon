# Generated by Django 3.1.12 on 2021-07-10 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_frozen',
            field=models.BooleanField(default=False),
        ),
    ]
