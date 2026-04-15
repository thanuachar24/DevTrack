from django.urls import path
from .views import create_reporter, create_issue, list_issues, list_reporters

urlpatterns = [
    path('reporters/', create_reporter, name='create_reporter'),
    path('issues/', create_issue, name='create_issue'),
    path('issues/list/', list_issues, name='list_issues'),
    path('reporters/list/', list_reporters, name='list_reporters'),
]