# Generated by Django 3.1.12 on 2021-09-03 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0003_auto_20210901_1808'),
        ('inventory', '0010_laborvendor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assembly',
            options={'ordering': ['part_number']},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['part_number']},
        ),
        migrations.AlterModelOptions(
            name='labor',
            options={'ordering': ['part_number']},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['part_number']},
        ),
        migrations.CreateModel(
            name='DocumentVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('list_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documentvendor_created_by', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.document')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documentvendor_modified_by', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]