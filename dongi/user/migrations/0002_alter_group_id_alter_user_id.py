# Generated by Django 5.1.5 on 2025-02-19 05:25

import django_ulid.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='id',
            field=django_ulid.models.ULIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=django_ulid.models.ULIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
