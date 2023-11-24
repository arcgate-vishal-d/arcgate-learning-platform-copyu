# Generated by Django 4.2.5 on 2023-11-03 07:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="role",
            field=models.IntegerField(
                choices=[
                    (1, "Super Admin"),
                    (2, "Project Manager"),
                    (3, "Assistant Project Manager"),
                    (4, "Team Lead"),
                    (5, "Agent"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="employee_id",
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
