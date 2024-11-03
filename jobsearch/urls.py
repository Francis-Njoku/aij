# jobsearch/urls.py
#from django.urls import path
from .views import JobSearchView
from django.urls import path, include

urlpatterns = [
    # Other app URLs
    path('search-jobs/', JobSearchView.as_view(), name='search-jobs'),
]
