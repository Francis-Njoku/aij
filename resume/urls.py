from django.urls import path
from .views import ResumeUploadView, UserProfileView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]