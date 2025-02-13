# Generated by Django 4.2.6 on 2025-02-07 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='expenseshare',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='payment',
            name='expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.expense'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='receipt',
            field=models.ImageField(blank=True, null=True, upload_to='receipts/'),
        ),
    ]
