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
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name='user'
    )
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume uploade on {self.uploaded_at}"