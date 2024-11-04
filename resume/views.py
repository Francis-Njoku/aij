from django.shortcuts import render
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserProfileSerializer, ResumeSerializer, JobExperienceSerializer
from .utils import extract_text_from_pdf, extract_keywords
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
#from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .models import UserProfile, JobExperience
from .utils import extract_text_from_pdf, extract_text_from_docx, parse_experience_and_education
from rest_framework import generics
from .models import Resume, UserProfile


# Create your views here.
'''
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
'''
class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = Resume.objects.create(user=request.user, file=serializer.validated_data['file'])
            file_path = resume.file.path  # Path of the uploaded resume file

            # Extract text based on file format
            if file_path.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file_path.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

            # Parse experience, education, and skills
            experience_text, education_text = parse_experience_and_education(text)
            skills = extract_keywords(text)

            # Update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.summary = experience_text[:500]  # Optional: truncated summary
            profile.education = [
                {"degree": degree.strip(), "institution": institution.strip(), "year": year.strip()}
                for degree, institution, year in re.findall(r"(Bachelor's|Master's|PhD).*?in.*?([A-Za-z\s]+).*?(\d{4})", education_text, re.IGNORECASE)
            ]
            profile.skills = ", ".join(skills)
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

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the UserProfile associated with the authenticated user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
class JobExperienceListView(generics.ListAPIView):
    serializer_class = JobExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobExperience.objects.filter(user=self.request.user)