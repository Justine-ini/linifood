# Generated by Django 5.0.6 on 2024-05-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_alter_order_is_ordered"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="is_ordered",
            field=models.BooleanField(default=False),
        ),
    ]
