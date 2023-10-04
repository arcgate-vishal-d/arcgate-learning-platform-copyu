from django.contrib import admin
from .models import UserData, UserPermission, Project, Role

# from account.apis.permissions import MyPermissions

admin.site.register(UserData)
admin.site.register(UserPermission)
admin.site.register(Project)
admin.site.register(Role)
# user.user_permissions.add(MyPermissions)
