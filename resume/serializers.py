from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Resume, JobSkill

User = get_user_model()

class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Resume
        fields = ['id','user','file','uploaded_at']