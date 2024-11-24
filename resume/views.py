from django.shortcuts import render
import os
import re
import json
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import JobSkillSerializer, UserProfileSerializer, ResumeSerializer, JobExperienceSerializer
from .utils import extract_text_from_pdf, extract_keywords
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
#from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .models import JobSkill, UserProfile, JobExperience
from .utils import extract_text_from_pdf, parse_experience, parse_education, extract_skills_from_text, extract_text_from_docx, parse_experience_and_education
from rest_framework import generics
from .models import Resume, UserProfile
from django.shortcuts import get_object_or_404

# Common words to exclude
COMMON_WORDS = {
    "and", "the", "of", "to", "in", "for", "on", "a", "by", "with",
    "at", "as", "is", "from", "or", "that", "an", "be", "are", "was",
    "were", "it", "this", "these", "not", "which", "has", "have", "will"
}

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
            profile.save()s,
                }
            }, status=status.HTTP_201_CRE

            return Response({
                "uploaded_file": serializer.data,
                "profile": {
                    "summary": profile.summary,
                    "education": profile.education,
                    "skills": profile.skillATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

@api_view(['GET'])
def job_skills(request):
    if request.method == 'GET':
        # Retrieve all job skills
        job_skills = JobSkill.objects.all()
        serializer = JobSkillSerializer(job_skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])  # Only admins can perform this request
def job_skill_list(request):
    if request.method == 'GET':
        # Retrieve all job skills
        job_skills = JobSkill.objects.all()
        serializer = JobSkillSerializer(job_skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create new job skills from the input
        serializer = JobSkillSerializer(data=request.data)
        if serializer.is_valid():
            job_skills = serializer.create(serializer.validated_data)
            response_data = JobSkillSerializer(job_skills, many=True).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])  # Only admins can perform this request
def job_skill_update(request, pk):
    try:
        job_skill = JobSkill.objects.get(pk=pk)
    except JobSkill.DoesNotExist:
        return Response({"error": "Job skill not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = JobSkillSerializer(instance=job_skill, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = Resume.objects.create(user=request.user, file=serializer.validated_data['file'])
            file_path = resume.file.path

            # Extract text from the file
            if file_path.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file_path.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract education, experience, and skills directly from the text
            education = parse_education(text)
            skills = extract_skills_from_text(text)
            experience = parse_experience(text)
            summary = text[:500]  # Take the first 500 characters as a summary

            # Update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.summary = summary
            profile.education = education  # Save as JSON
            profile.skills = ", ".join(skills)  # Store skills as comma-separated string
            profile.save()

            return Response({
                "uploaded_file": serializer.data,
                "profile": {
                    "summary": profile.summary,
                    "education": profile.education,
                    "skills": profile.skills,
                },
                "experience": experience
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
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
'''
        
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
    

# Create JobExperience
class JobExperienceCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = JobExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update JobExperience
class JobExperienceUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            job_experience = JobExperience.objects.get(pk=pk, user=request.user)
        except JobExperience.DoesNotExist:
            return Response({"error": "Job experience not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobExperienceSerializer(job_experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete JobExperience
class JobExperienceDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            job_experience = JobExperience.objects.get(pk=pk, user=request.user)
        except JobExperience.DoesNotExist:
            return Response({"error": "Job experience not found"}, status=status.HTTP_404_NOT_FOUND)

        job_experience.delete()
        return Response({"message": "Job experience deleted successfully"}, status=status.HTTP_204_NO_CONTENT)    
    

# Utility function to clean and deduplicate skills
def extract_skills(text):
    if not text:
        return ""

    # Split skills by commas, strip whitespace, and filter out common words
    skills = [skill.strip() for skill in text.split(",") if skill.strip()]
    filtered_skills = [
        skill for skill in skills
        if all(word.lower() not in COMMON_WORDS for word in skill.split())
    ]

    # Remove duplicates while preserving order
    seen = set()
    deduplicated_skills = [skill for skill in filtered_skills if not (skill.lower() in seen or seen.add(skill.lower()))]

    return ", ".join(deduplicated_skills)

class AdminUpdateSkillsView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the user ID from the URL or request data
        user_id = kwargs.get('user_id')
        user_profile = get_object_or_404(UserProfile, user_id=user_id)

        # Get the new skills data from the request
        new_skills = request.data.get('skills', '')
        if not new_skills:
            return Response({"error": "No skills provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Process and clean skills
        cleaned_skills = extract_skills(new_skills)

        # Update the user's profile
        user_profile.skills = cleaned_skills
        user_profile.save()

        return Response({
            "message": "Skills updated successfully",
            "skills": cleaned_skills
        }, status=status.HTTP_200_OK)\
        
class UpdateSkillsView(APIView):
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def post(self, request, *args, **kwargs):
        # Get the authenticated user's profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Get the new skills data from the request
        new_skills = request.data.get('skills', '')
        if not new_skills:
            return Response({"error": "No skills provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Process and clean skills
        cleaned_skills = extract_skills(new_skills)

        # Update the user's profile
        user_profile.skills = cleaned_skills
        user_profile.save()

        return Response({
            "message": "Skills updated successfully",
            "skills": cleaned_skills
        }, status=status.HTTP_200_OK)