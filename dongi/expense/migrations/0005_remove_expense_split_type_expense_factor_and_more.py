# Generated by Django 5.1.5 on 2025-02-21 18:25

import django_ulid.models
import ulid.api.api
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_alter_expense_id_alter_expenseshare_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='split_type',
        ),
        migrations.AddField(
            model_name='expense',
            name='factor',
            field=models.ImageField(blank=True, null=True, upload_to='factors/'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='expenseshare',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False),
        ),
    ]
