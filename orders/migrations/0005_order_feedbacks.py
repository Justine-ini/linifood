# Generated by Django 5.0.6 on 2024-05-30 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0004_alter_order_is_ordered"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="feedbacks",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
