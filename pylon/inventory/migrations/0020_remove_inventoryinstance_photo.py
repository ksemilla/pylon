# Generated by Django 3.1.12 on 2021-09-05 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_assemblyitemdocument_assemblyitemlabor_assemblyitemstock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryinstance',
            name='photo',
        ),
    ]
