# Generated by Django 4.2.5 on 2023-10-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="employee_id",
            field=models.CharField(default="True", max_length=30, unique=True),
        ),
    ]
