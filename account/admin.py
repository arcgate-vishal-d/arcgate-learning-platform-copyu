from django.contrib import admin
from .models import User_data, User_permission, Project, Role

# Register your models here.
admin.site.register(User_data)
# Register your models here.
admin.site.register(User_permission)
# Register your models here.
admin.site.register(Project)

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('role', 'ROLE_CHOICES')
admin.site.register(Role)
         