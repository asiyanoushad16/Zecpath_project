from django.urls import path

from .views import (
    TestAPIView,
    SignupAPIView,
    LogoutAPIView,
    JobListAPIView,
    JobCreateAPIView,
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
]