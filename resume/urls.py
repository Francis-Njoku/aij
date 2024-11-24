from django.urls import path
from .views import job_skill_list, job_skill_update, AdminUpdateSkillsView, UpdateSkillsView, JobExperienceListView, JobExperienceCreateView, JobExperienceDeleteView, JobExperienceUpdateView, ResumeUploadView, UserProfileView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('job-experiences/create/', JobExperienceCreateView.as_view(), name='jobexperience-create'),
    path('job-experiences/update/<int:pk>/', JobExperienceUpdateView.as_view(), name='jobexperience-update'),
    path('job-experiences/delete/<int:pk>/', JobExperienceDeleteView.as_view(), name='jobexperience-delete'),
    path('job-experiences/', JobExperienceListView.as_view(), name='jobexperience-list'),
    path('admin/profile/update-skills/<int:user_id>/', UpdateSkillsView.as_view(), name='admin-update-skills'),
    path('profile/update-skills/', UpdateSkillsView.as_view(), name='update-skills'),
    path('admin/job-skills/', job_skill_list, name='job-skill-list'),
    path('admin/job-skills/<int:pk>/', job_skill_update, name='job-skill-update'),
]