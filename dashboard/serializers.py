
from rest_framework import serializers

from dashboard.models import Video, Dashboard
from account.models import Project
from account.apis.serializers import ProjectsSerializer

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class DashboardSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(source="users.id")
    videos = VideoSerializer()
    projects = ProjectsSerializer()
    # role = serializers.CharField(source="role.get_role_display")

    class Meta:
        model = Dashboard
        fields = [
            "videos",
            "projects",
        ]