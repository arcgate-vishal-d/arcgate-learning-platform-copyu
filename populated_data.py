"""

If you want to delete all the records in the database run this command
"python manage.py flush"

then run the script

"python populated_data.py

"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arc_learning_platform.settings")
django.setup()

from account.models import Role, Project, User, Permission, UserData

roles_data = [
    {"role": 1},
    {"role": 2},
    {"role":3},
    {"role": 4},
    {"role": 5},
]

for data in roles_data:
    role, created = Role.objects.get_or_create(role=data["role"])

projects_data = [
    {"project_name": "Payroll", "project_slug": "project-1111"},
    {"project_name": "Amazon", "project_slug": "project-2111"},
    {"project_name": "Jio Mart", "project_slug": "project-3111"},
    {"project_name": "Swiggy", "project_slug": "project-4111"},
]

for data in projects_data:
    Project.objects.create(**data)

users_data = [
    {"username": "user111", "email": "user111@example.com", "employee_id": "emp_05"},
    {"username": "user112", "email": "user112@example.com", "employee_id": "emp_06"},
    {"username": "user113", "email": "user113@example.com", "employee_id": "emp_07"},
]

for data in users_data:
    user, created = User.objects.get_or_create(
        username=data["username"],
        defaults={"email": data["email"], "employee_id": data["employee_id"]},
    )
    if created:
        user.set_password("Test@123")
        user.is_superuser = True
        user.is_staff = True
        user.save()


permissions_data = [
    {"read": True, "delete": False, "update": True},
    {"read": True, "delete": True, "update": False},
]

for data in permissions_data:
    Permission.objects.create(**data)


user_data = [
    {
        "users": User.objects.get(username="user111"),
        "project": Project.objects.get(project_slug="project-1111"),
        "role": Role.objects.get(role=1),
        "permissions": Permission.objects.get(read=True, delete=False, update=True),
    },
    {
        "users": User.objects.get(username="user112"),
        "project": Project.objects.get(project_slug="project-2111"),
        "role": Role.objects.get(role=2),
        "permissions": Permission.objects.get(read=True, delete=True, update=False),
    },
    {
        "users": User.objects.get(username="user111"),
        "project": Project.objects.get(project_slug="project-2111"),
        "role": Role.objects.get(role=3),
        "permissions": Permission.objects.get(read=True, delete=True, update=False),
    },
    {
        "users": User.objects.get(username="user111"),
        "project": Project.objects.get(project_slug="project-3111"),
        "role": Role.objects.get(role=2),
        "permissions": Permission.objects.get(read=True, delete=True, update=False),
    },
    {
        "users": User.objects.get(username="user112"),
        "project": Project.objects.get(project_slug="project-1111"),
        "role": Role.objects.get(role=3),
        "permissions": Permission.objects.get(read=True, delete=True, update=False),
    },
]

for data in user_data:
    UserData.objects.create(**data)
