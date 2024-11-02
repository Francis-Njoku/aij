from django.db import models
from django.conf import settings
from django.utils.text import slugify
from authentication.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class JobSkill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, null=True, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume uploade on {self.uploaded_at}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    education = models.TextField(blank=True, null=True)  # E.g., "Bachelor's in Computer Science, XYZ University"
    skills = models.TextField(blank=True, null=True)  # E.g., "Python, Django, Machine Learning"
    summary = models.TextField(blank=True, null=True)  # Brief summary from the CV

class JobExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_experiences")
    title = models.CharField(max_length=255)  # Job title
    company = models.CharField(max_length=255)  # Company name
    responsibilities = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)    