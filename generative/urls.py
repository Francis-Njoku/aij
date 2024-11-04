from django.urls import path
from .views import GenerateCoverLetterView, InterviewQuestionView, UserInterviewQuestionsView

urlpatterns = [
    path('generate-cover-letter/', GenerateCoverLetterView.as_view(), name='generate-cover-letter'),
    path('generate-questions/', InterviewQuestionView.as_view(), name='generate-questions'),
    path('user/<int:user_id>/questions/', UserInterviewQuestionsView.as_view(), name='user-questions'),
]