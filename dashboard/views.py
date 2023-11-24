from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import time

from dashboard.models import Video, Dashboard
from dashboard.serializers import DashboardSerializer, VideoSerializer
from account.models import Project
from account.apis.serializers import ProjectsSerializer

from rest_framework import status

class VideoUploadView(APIView):
        
    def post(self, request):
        pass
        video_file = request.data['file']

        if video_file.content_type.startswith('video'):
            try:
                with VideoFileClip(video_file.temporary_file_path()) as video_clip:
                    video_duration = video_clip.duration
            except Exception as e:
                print(f"Error getting video duration: {str(e)}")
                video_duration = None

            if video_duration is not None:
                chunk_duration_seconds = 10  # Set your desired chunk duration in seconds
                video_name = os.path.splitext(video_file.name)[0]

                # Create a folder for the video chunks
                output_folder = f'media/video_chunks/{video_name}/'
                os.makedirs(output_folder, exist_ok=True)

                # Process or save each chunk as needed
                start_time = 0
                chunk_number = 1
                while start_time < video_duration:
                    end_time = min(start_time + chunk_duration_seconds, video_duration)
                    timestamp = int(time.time())  # Generate a timestamp for uniqueness
                    output_file = f'chunk_{chunk_number}_{timestamp}.mp4'
                    ffmpeg_extract_subclip(video_file.temporary_file_path(), start_time, end_time, targetname=os.path.join(output_folder, output_file))
                    start_time = end_time
                    chunk_number += 1

                return Response({'message': 'Video file chunked by seconds successfully'})

        return Response({'message': 'Invalid file format. Please upload a video file.'}, status=400)


class DashboardView(APIView):

    def get(self, request):
        videos = Video.objects.all()
        project = Project.objects.all()
        serializer = VideoSerializer(videos, many=True)
        project = ProjectsSerializer(project, many=True)
        response_data = {
            "video": serializer.data[0],
            "project": project.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)