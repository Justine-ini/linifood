# Generated by Django 5.0.6 on 2024-05-17 14:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_user_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(1, "vendor"), (2, "customer")], null=True
            ),
        ),
    ]