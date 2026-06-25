from django.urls import path

from .views import (
    TestAPIView,
    SignupAPIView,
    LogoutAPIView,
    JobListAPIView,
    JobCreateAPIView,
    CandidateAPIView,
    AdminAPIView,
    ApplyJobAPIView,
    CandidateProfileAPIView,
    EmployerProfileAPIView,
    ResumeUploadAPIView,
    UserListAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('test/', TestAPIView.as_view()),

    path('signup/', SignupAPIView.as_view()),

    path(
        'login/',
        TokenObtainPairView.as_view()
    ),

    path(
        'refresh/',
        TokenRefreshView.as_view()
    ),

    path(
        'logout/',
        LogoutAPIView.as_view()
    ),

    path(
        'jobs/',
        JobListAPIView.as_view()
    ),

    path(
        'jobs/create/',
        JobCreateAPIView.as_view()
    ),
    
    path(
    'candidate/',
    CandidateAPIView.as_view()
   ),

path(
    'admin-dashboard/',
    AdminAPIView.as_view()
   ),
path(
    'jobs/<int:job_id>/apply/',
    ApplyJobAPIView.as_view()
),

path(
    'candidate/profile/',
    CandidateProfileAPIView.as_view()
),

path(
    'employer/profile/',
    EmployerProfileAPIView.as_view()
),
path(
    'candidate/upload-resume/',
    ResumeUploadAPIView.as_view()
),
path(
    'users/',
    UserListAPIView.as_view()
),
]