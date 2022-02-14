# Generated by Django 3.1.12 on 2021-09-20 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0025_auto_20210909_0937'),
        ('quotations', '0002_quotation_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.CreateModel(
            name='QuotationItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(choices=[('s', 'Stock'), ('l', 'Labor'), ('d', 'Document'), ('a', 'Assembly')], default='s', max_length=64)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('list_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('sell_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotationitem_created_by', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_item', to='inventory.inventory')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotationitem_modified_by', to=settings.AUTH_USER_MODEL)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotations.quotation')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='QuotationAssemblyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(choices=[('s', 'Stock'), ('l', 'Labor'), ('d', 'Document')], default='s', max_length=64)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('list_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('sell_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotationassemblyitem_created_by', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotationassembly_item', to='inventory.inventory')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotationassemblyitem_modified_by', to=settings.AUTH_USER_MODEL)),
                ('quotation_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotations.quotationitem')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]