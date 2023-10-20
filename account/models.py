from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class AbstractTable(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(AbstractTable):
    superadmin = 1
    project_manager = 2
    assistant_project_manager = 3
    team_lead = 4
    agent = 5

    ROLE_CHOICES = (
        (superadmin, "Super Admin"),
        (project_manager, "Project Manager"),
        (assistant_project_manager, "Assistant Project Manager"),
        (team_lead, "Team Lead"),
        (agent, "Agent"),
    )

    role = models.IntegerField(choices=ROLE_CHOICES)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return f"{self.get_role_display()}"


class Project(AbstractTable):
    project_name = models.CharField(max_length=200)
    project_slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return str(self.project_name)


class User(AbstractUser):
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(unique=True, default="True", max_length=30)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "employee_id"]

    def __str__(self):
        return self.email


class Permission(AbstractTable):
    read = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)

    class Meta:
        db_table = "permissions"


class UserData(AbstractTable):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permissions = models.ForeignKey(Permission, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=False, blank=False, default=True)
    status = models.BooleanField(default=True)

    # STATUS_CHOICES = ((0, "Active"), (1, "Inactive"))
    # status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        db_table = "user_data"

    # def get_status_display(self):
    #     return dict(UserData.STATUS_CHOICES).get(self.status, self.status)

    def __str__(self):
        return str(self.users.username)
