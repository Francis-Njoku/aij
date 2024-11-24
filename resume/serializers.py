from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Resume, JobSkill, JobExperience, UserProfile

User = get_user_model()

class ResumeSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Resume
        fields = ['file']

class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = ['id', 'user', 'title', 'company', 'start_date', 'end_date', 'responsibilities']
        read_only_fields = ['user']  # Make 'user' read-only since we'll set it in the view  

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'education', 'skills', 'summary']
        read_only_fields = ['user']

    def validate_skills(self, value):
        # Split skills by comma and remove extra whitespace
        return [skill.strip() for skill in value.split(',') if skill.strip()]

    def to_representation(self, instance):
        # Override to split skills into a list in the response
        representation = super().to_representation(instance)
        if representation['skills']:
            representation['skills'] = representation['skills'].split(',')
        return representation   
    
class JobSkillSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError({"name": "This field is required."})
        
        # Split the comma-separated names
        names = data['name'].split(', ')
        if any(len(name.strip()) > 100 for name in names):
            raise serializers.ValidationError(
                {"name": "Each job skill must not exceed 100 characters."}
            )
        return data

    def create(self, validated_data):
        names = validated_data['name'].split(', ')
        job_skills = []
        for name in names:
            job_skill, created = JobSkill.objects.get_or_create(name=name.strip())
            job_skills.append(job_skill)
        return job_skills
               