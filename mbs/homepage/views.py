from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.urls import reverse
from administration.models import FrontendBanner, YoutubeVideos
from employee.models import EmployeeFrontendProfile
import requests
from django.http import JsonResponse
import json

# Create your views here.

def homepage(request):
    form = ContactForm()

    #get all the banners
    banners = FrontendBanner.objects.filter(selected=1).order_by('-created_at')

    #get all team members
    members = EmployeeFrontendProfile.objects.all()

    extracted_videos = YoutubeVideos.objects.order_by('-created_at')[:3]
    
    context = {
        'form' : form,
        'banners':banners,
        'members' : members,
        'extractedVideos' : extracted_videos
    }
    return render(request, 'homeindex.html', context)

def contactFormPost(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us, we will get back to your in 48 business hours.')
            return redirect(reverse('homepage')+ '#contact')
        else:
            messages.success(request, 'Error in submitting the form. Please try again..')
            return redirect(reverse('homepage')+ '#contact')
            
def testPage(request):
    return render(request, 'hair_botox_repair.html')

def youtube_videos(request):
    API_KEY = 'AIzaSyBEU5WIAmGTRzDrPhN1NLnKBGOpupQBgFc'  # Replace with your API Key
    CHANNEL_ID = 'UC6sZSwgahzSM3htoVgwv8CA'    # Replace with your Channel ID
    MAX_RESULTS = 3  # Number of videos to fetch

    # YouTube API URL
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults={MAX_RESULTS}"

    try:
        # Make request to YouTube API
        response = requests.get(url)
        data = response.json()
        extracted_video = []
        for i in data.get('items', []):
            titleTemp = i['snippet']['title']
            thumbnailTemp = i['snippet']['thumbnails']['medium']['url']
            videoIdTemp = i['id'].get('videoId')
            extracted_video.append({
                'title': titleTemp,
                'thumbnail': thumbnailTemp,
                'url': f"https://www.youtube.com/watch?v={videoIdTemp}"
            })
        return extracted_video
    except Exception as e:
        data = []
        return data