# interview/serializers.py
from rest_framework import serializers
from .models import InterviewQuestion
from .models import CoverLetter

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ['id', 'user', 'skill', 'question', 'answer', 'created_at']

class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ['id', 'user', 'job_title', 'company_name', 'cover_letter_text', 'created_at']        