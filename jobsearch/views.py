from django.shortcuts import render

# Create your views here.
# jobsearch/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .utils import search_jobs
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from resume.models import UserProfile  # Assuming UserProfile contains the user's skills
from rest_framework.decorators import permission_classes


@permission_classes([IsAuthenticated])  # Only admins can upload and update
class JobSearchView(APIView):
    def get(self, request):
        user = request.user
        profile = user.userprofile  # Assuming each user has a UserProfile
        
         # Check the skills before querying
        skills = profile.skills.split(', ') if profile.skills else []
        print("Skills extracted:", skills)
        
        if not skills:
            return Response({"error": "No skills found for the user"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Call the Google Search API
        api_key = settings.GOOGLE_SEARCH_API_KEY
        cse_id = settings.GOOGLE_CSE_ID
        job_results = search_jobs(skills, api_key, cse_id)
        
        return Response({"jobs": job_results}, status=status.HTTP_200_OK)

