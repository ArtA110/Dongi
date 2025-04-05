# Generated by Django 5.1.5 on 2025-04-05 08:26

import core.models
import core.validators.field_validators
import django_ulid.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', django_ulid.models.ULIDField(default=core.models.new_ulid, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('bought_at', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('split_data', models.JSONField(blank=True, null=True, validators=[core.validators.field_validators.JSONSchemaValidator(limit_value={'$schema': 'https://json-schema.org/draft/2020-12/schema#', 'properties': {'users': {'description': 'List of users and their respective amounts', 'items': {'properties': {'amount': {'description': 'Amount that should be paid by the user', 'type': 'number'}, 'user_id': {'description': 'User ID of the user', 'type': 'string'}}, 'required': ['user_id', 'amount'], 'type': 'object'}, 'type': 'array'}}, 'required': ['users'], 'type': 'object'})])),
                ('factor', models.ImageField(blank=True, null=True, upload_to='dongi/expense/factors/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseShare',
            fields=[
                ('id', django_ulid.models.ULIDField(default=core.models.new_ulid, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', django_ulid.models.ULIDField(default=core.models.new_ulid, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('paid_at', models.DateTimeField(auto_now_add=True)),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='dongi/expense/receipts/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
