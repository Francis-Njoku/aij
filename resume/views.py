from django.shortcuts import render
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
#from .models import Resume
from .serializers import ResumeSerializer, JobExperienceSerializer
from .utils import extract_text_from_pdf, extract_keywords
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
#from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .models import UserProfile, JobExperience
from .utils import extract_text_from_pdf, parse_experience_and_education
from rest_framework import generics
from .models import Resume, UserProfile


# Create your views here.
class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            # Create the Resume instance with user information
            resume = Resume.objects.create(user=request.user, file=serializer.validated_data['file'])
            file_path = resume.file.path  # Path of the uploaded resume file

            # Extract text from the PDF and parse experience/education details
            text = extract_text_from_pdf(file_path)
            experience_text, education_text = parse_experience_and_education(text)

            # Update user profile with parsed details
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.summary = experience_text[:500]  # Optional summary from the text
            profile.education = education_text
            profile.skills = ", ".join(extract_keywords(text))
            profile.save()

            return Response({
                "uploaded_file": serializer.data,
                "profile": {
                    "summary": profile.summary,
                    "education": profile.education,
                    "skills": profile.skills,
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        resumes = Resume.objects.filter(user=user)
        resume_serializer = ResumeSerializer(resumes, many=True)

        return Response({
            "profile": {
                "summary": profile.summary,
                "education": profile.education,
                "skills": profile.skills,
            },
            "resumes": resume_serializer.data,
        })

class JobExperienceListView(generics.ListAPIView):
    serializer_class = JobExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobExperience.objects.filter(user=self.request.user)