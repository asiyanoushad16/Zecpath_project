from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Job,
    Candidate,
    Employer,
    Application
)

from .serializers import (
    JobSerializer,
    RegisterSerializer,
    CandidateSerializer,
    EmployerSerializer,
    ResumeSerializer
)

from .permissions import (
    IsAdmin,
    IsEmployer,
    IsCandidate
)


class TestAPIView(APIView):

    def get(self, request):
        return Response({
            "message": "Hello DRF"
        })


class SignupAPIView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User created successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data["refresh"]

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response({
                "message": "Logout successful"
            })

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class JobListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        jobs = Job.objects.all()

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)


class JobCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def post(self, request):

        serializer = JobSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CandidateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def get(self, request):

        return Response({
            "message": "Candidate Dashboard"
        })


class AdminAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        return Response({
            "message": "Admin Dashboard"
        })


class ApplyJobAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def post(self, request, job_id):

        job = Job.objects.get(id=job_id)

        candidate = Candidate.objects.get(
            user=request.user
        )

        Application.objects.create(
            candidate=candidate,
            job=job
        )

        return Response({
            "message": "Applied successfully"
        })


class CandidateProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    # Create Profile
    def post(self, request):

        if Candidate.objects.filter(
            user=request.user
        ).exists():

            return Response(
                {
                    "error": "Profile already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CandidateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # View Profile
    def get(self, request):

        candidate = Candidate.objects.get(
            user=request.user
        )

        serializer = CandidateSerializer(
            candidate
        )

        return Response(serializer.data)

    # Update Profile
    def put(self, request):

        candidate = Candidate.objects.get(
            user=request.user
        )

        serializer = CandidateSerializer(
            candidate,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Soft Delete
    def delete(self, request):

        candidate = Candidate.objects.get(
            user=request.user
        )

        candidate.is_active = False
        candidate.save()

        return Response(
            {
                "message": "Profile deactivated successfully."
            }
        )


class EmployerProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    # Create Profile
    def post(self, request):

        if Employer.objects.filter(
            user=request.user
        ).exists():

            return Response(
                {
                    "error": "Profile already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EmployerSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # View Profile
    def get(self, request):

        employer = Employer.objects.get(
            user=request.user
        )

        serializer = EmployerSerializer(
            employer
        )

        return Response(serializer.data)

    # Update Profile
    def put(self, request):

        employer = Employer.objects.get(
            user=request.user
        )

        serializer = EmployerSerializer(
            employer,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Soft Delete
    def delete(self, request):

        employer = Employer.objects.get(
            user=request.user
        )

        employer.is_active = False
        employer.save()

        return Response(
            {
                "message": "Profile deactivated successfully."
            }
        )
class ResumeUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    def post(self, request):

        candidate = Candidate.objects.get(
            user=request.user
        )

        serializer = ResumeSerializer(
            candidate,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Resume uploaded successfully",
                    "resume": candidate.resume.url
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )