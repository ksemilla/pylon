# Generated by Django 3.1.12 on 2021-09-01 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_vendor_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['code']},
        ),
        migrations.AlterModelOptions(
            name='vendoraddress',
            options={'ordering': ['-is_primary']},
        ),
    ]