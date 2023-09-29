from django.contrib import admin
from .models import UserData, UserPermission, Project, Role

admin.site.register(UserData)
admin.site.register(UserPermission)
admin.site.register(Project)
admin.site.register(Role)
