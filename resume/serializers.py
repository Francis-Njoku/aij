from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Resume, JobSkill, JobExperience

User = get_user_model()

class ResumeSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Resume
        fields = ['file']

class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = ['id', 'user', 'job_title', 'company', 'start_date', 'end_date', 'responsibilities']
        read_only_fields = ['user']  # Make 'user' read-only since we'll set it in the view        