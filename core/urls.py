from django.urls import path

from .views import (
    TestAPIView,
    JobListAPIView,
    JobCreateAPIView
)

urlpatterns = [
    path('test/', TestAPIView.as_view()),
    path('jobs/', JobListAPIView.as_view()),
    path('jobs/create/', JobCreateAPIView.as_view()),
]