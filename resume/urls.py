from django.urls import path
from .views import JobExperienceListView, JobExperienceCreateView, JobExperienceDeleteView, JobExperienceUpdateView, ResumeUploadView, UserProfileView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('job-experiences/create/', JobExperienceCreateView.as_view(), name='jobexperience-create'),
    path('job-experiences/update/<int:pk>/', JobExperienceUpdateView.as_view(), name='jobexperience-update'),
    path('job-experiences/delete/<int:pk>/', JobExperienceDeleteView.as_view(), name='jobexperience-delete'),
    path('job-experiences/', JobExperienceListView.as_view(), name='jobexperience-list'),
]