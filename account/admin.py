from django.contrib import admin
from .models import UserData, UserPermission, Project, Role

# Register your models here.
admin.site.register(UserData)
# Register your models here.
admin.site.register(UserPermission)
# Register your models here.
admin.site.register(Project)

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('role', 'ROLE_CHOICES')
admin.site.register(Role)
