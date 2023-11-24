from django.db import models

from account.models import *
from account.models import AbstractTable


class Video(AbstractTable):
    file = models.FileField(upload_to='videos/')
    upload_date = models.DateTimeField(auto_now_add=True)

class Dashboard(models.Model):
    videos = models.ForeignKey(Video, on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    

    def __str__(self):
        return self.user.username
    


