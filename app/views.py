from django.shortcuts import render,redirect
from pythumb import Thumbnail
import os
import urllib
from django.http import HttpResponse
from googleapiclient.discovery import build
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context
YOUTUBE_API_KEY = "AIzaSyArSVZceKfiM5zj5JI7L8f7RUpUw0Kcuo8"

def index(request):
    return render(request, 'index.html')


from googleapiclient.discovery import build
import urllib.request
from django.http import HttpResponse

api_key = 'AIzaSyArSVZceKfiM5zj5JI7L8f7RUpUw0Kcuo8' 
youtube = build('youtube', 'v3', developerKey=api_key)


def download_thumbnail(thumbnail_url, file_name):
    urllib.request.urlretrieve(thumbnail_url, file_name)
    print(f'Thumbnail image downloaded as {file_name}')

def get_youtube_thumbnail(request):
    if request.method == 'POST':
        pattern = r"(?<=v=)[a-zA-Z0-9_-]{11}|(?<=be/)[a-zA-Z0-9_-]{11}"
        video_url = request.POST['url']
        match = re.search(pattern, video_url)
        video_id = match.group(0)
        if video_id:
            part = 'snippet'
            fields = 'items(snippet(thumbnails(standard,high)))'
            response = youtube.videos().list(
                part=part,
                id=video_id,
                fields=fields
            ).execute()
            thumbnails = response['items'][0]['snippet']['thumbnails']
            thumbnail_url = thumbnails['standard']['url'] 
            print(thumbnail_url)


            return render(request,'index.html',{"thumbnail_url":thumbnail_url})

            # download_thumbnail(thumbnail_url, 'thumbnail.jpg') 
            


            # with open('thumbnail.jpg', 'rb') as thumbnail_file:
            #     response = HttpResponse(thumbnail_file, content_type='image/jpeg')
            #     response['Content-Disposition'] = 'attachment; filename="thumbnail.jpg"'
            #     return response
                
            
        else:
            return HttpResponse('video_id parameter is missing')
    else:
        return HttpResponse('Invalid request')


    




