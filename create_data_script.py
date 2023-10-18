import random
from django.contrib.auth.models import User
from account.models import Role, Project, Permission, UserData
from django.utils import timezone
from faker import Faker

import os
import django
from django.conf import settings

settings.configure()
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arc_learning_platform.settings")

# Initialize Django
django.setup()

fake = Faker()

def create_roles():
    roles = [
        "Super Admin",
        "Project Manager",
        "Assistant Project Manager",
        "Team Lead",
        "Agent",
    ]
    for role in roles:
        Role.objects.get_or_create(role=role)

def create_projects():
    for _ in range(10):
        project_name = fake.word()
        project_slug = project_name.lower()
        Project.objects.get_or_create(project_name=project_name, project_slug=project_slug)

def create_users_and_user_data():
    for _ in range(10):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(username=username, email=email, password=password)
        
    roles = Role.objects.all()
    projects = Project.objects.all()
    permissions = Permission.objects.all()
    users = User.objects.all()

    for _ in range(10):
        role = random.choice(roles)
        project = random.choice(projects)
        permission = random.choice(permissions)
        user = random.choice(users)
        fullname = fake.name()
        status = random.choice(["Active", "Inactive"])

        UserData.objects.create(
            users=user,
            project=project,
            role=role,
            permissions=permission,
            fullname=fullname,
            status=status,
        )

if __name__ == "__main__":
    create_roles()
    create_projects()
    create_users_and_user_data()
