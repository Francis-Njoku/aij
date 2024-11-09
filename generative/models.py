# interview/models.py
from django.db import models
from authentication.models import User

class InterviewQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_questions')
    skill = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question for {self.user.username}: {self.question[:50]}..."

class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    cover_letter_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cover Letter for {self.job_title} at {self.company_name} by {self.user.username}"