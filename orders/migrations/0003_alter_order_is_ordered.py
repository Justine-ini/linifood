# Generated by Django 5.0.6 on 2024-05-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_remove_payment_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="is_ordered",
            field=models.BooleanField(default=True),
        ),
    ]
