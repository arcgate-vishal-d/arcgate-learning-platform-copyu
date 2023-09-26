from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class AbstractTable(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(AbstractTable):
    project_name = models.CharField(max_length=200, null=True, blank=True)
    project_slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return str(self.project_name)


class User_permission(AbstractTable):
    emp_id = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    update = models.BooleanField(default=False)

    class Meta:
        db_table = "user_permissions"

    def __str__(self):
        return str(self.emp_id)


class Role(AbstractTable):
    SUPERADMIN = 1
    PROJECT_MANAGER = 2
    ASSISTANT_PROJECT_MANAGER = 3
    TEAM_LEAD = 4
    AGENT = 5

    ROLE_CHOICES = (
        (SUPERADMIN, "Super Admin"),
        (PROJECT_MANAGER, "Project Manager"),
        (ASSISTANT_PROJECT_MANAGER, "Assistant Project Manager"),
        (TEAM_LEAD, "Team Lead"),
        (AGENT, "Agent"),
    )
    role = models.IntegerField(choices=ROLE_CHOICES)
    permission = models.ForeignKey(User_permission, on_delete=models.CASCADE)

    class Meta:
        db_table = "roles"

    def get_role_display_str(self):
        return ", ".join(
            [
                role_str
                for role_val, role_str in self.ROLE_CHOICES
                if role_val == self.role
            ]
        )

    def __str__(self):
        return f"{self.get_role_display_str()}"


class User_data(AbstractTable):
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    permission = models.ForeignKey(
        User_permission,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "user_datas"

    def __str__(self):
        return str(self.users)
