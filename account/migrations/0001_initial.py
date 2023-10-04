# Generated by Django 4.2.5 on 2023-10-04 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "project_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("project_slug", models.SlugField(max_length=200, unique=True)),
            ],
            options={
                "db_table": "projects",
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.IntegerField(
                        choices=[
                            (1, "Super Admin"),
                            (2, "Project Manager"),
                            (3, "Assistant Project Manager"),
                            (4, "Team Lead"),
                            (5, "Agent"),
                        ]
                    ),
                ),
            ],
            options={
                "db_table": "roles",
            },
        ),
        migrations.CreateModel(
            name="UserPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("emp_id", models.CharField(max_length=100, unique=True)),
                ("read", models.BooleanField(default=False)),
                ("delete", models.BooleanField(default=False)),
                ("update", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "user_permissions",
            },
        ),
        migrations.CreateModel(
            name="UserData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("fullName", models.CharField(default="", max_length=50)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Active"), (0, "Inactive")], default=False
                    ),
                ),
                (
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.userpermission",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_data",
                        to="account.project",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="account.role"
                    ),
                ),
                (
                    "users",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "user_datas",
            },
        ),
        migrations.AddField(
            model_name="role",
            name="permission",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="account.userpermission"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="role",
            unique_together={("role", "permission")},
        ),
    ]
