from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from .serializers import UserSerializer
from django.db.models import Count


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
    ResumeSerializer,
    UserSerializer,
    ApplicationSerializer
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




class JobCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def post(self, request):

        employer = Employer.objects.get(
            user=request.user
        )

        serializer = JobSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                employer=employer
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class JobUpdateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def put(self, request, job_id):

        employer = Employer.objects.get(
            user=request.user
        )

        job = Job.objects.get(
            id=job_id
        )

        if job.employer != employer:

            return Response(
                {
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class JobStatusAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def put(self, request, job_id):

        employer = Employer.objects.get(
            user=request.user
        )

        job = Job.objects.get(
            id=job_id
        )

        if job.employer != employer:

            return Response(
                {
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        job.is_active = not job.is_active
        job.save()

        return Response(
            {
                "message": "Job status updated successfully",
                "is_active": job.is_active
            }
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

        job = Job.objects.get(
            id=job_id
        )

        if not job.is_active:

            return Response(
                {
                    "error": "This job is no longer active."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        candidate = Candidate.objects.get(
            user=request.user
        )

        if Application.objects.filter(
            candidate=candidate,
            job=job
        ).exists():

            return Response(
                {
                    "error": "You have already applied for this job."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        Application.objects.create(
            candidate=candidate,
            job=job,
            resume_snapshot=candidate.resume
        )

        return Response(
            {
                "message": "Applied successfully"
            },
            status=status.HTTP_201_CREATED
        )


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
class JobPagination(PageNumberPagination):

    page_size = 5


class JobListAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Job.objects.select_related(
        'employer'
    ).filter(
        is_active=True
    )

    serializer_class = JobSerializer

    pagination_class = JobPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]

    filterset_fields = {
        'experience': ['exact', 'gte', 'lte'],
        'salary': ['exact', 'gte', 'lte'],
        'location': ['exact'],
        'job_type': ['exact']
    }

    search_fields = [
        'title',
        'skills',
        'description'
    ]
    


class LatestJobAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = JobSerializer

    pagination_class = JobPagination

    queryset = Job.objects.select_related(
        'employer'
    ).filter(
        is_active=True
    ).order_by(
        '-created_at'
    )[:10]
    
class FeaturedJobAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Job.objects.select_related(
        'employer'
    ).filter(
        featured=True,
        is_active=True
    )

    serializer_class = JobSerializer

    pagination_class = JobPagination


class UserListAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    serializer_class = UserSerializer

    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = [
        'role'
    ]
class ApplicationHistoryAPIView(ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsCandidate
    ]

    serializer_class = ApplicationSerializer

    def get_queryset(self):

        candidate = Candidate.objects.get(
            user=self.request.user
        )

        return Application.objects.select_related(
            'job',
            'candidate'
        ).filter(
            candidate=candidate
        ).order_by(
            '-applied_at'
        )
class ApplicationStatusAPIView(APIView):
 def put(self, request, application_id):

    employer = Employer.objects.get(
        user=request.user
    )

    application = Application.objects.get(
        id=application_id
    )

    if application.job.employer != employer:

        return Response(
            {
                "error": "Permission denied."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    new_status = request.data.get("status")

    valid_transitions = {

        "Applied": [
            "Under Review",
            "Rejected"
        ],

        "Under Review": [
            "Shortlisted",
            "Rejected"
        ],

        "Shortlisted": [
            "Interview Scheduled",
            "Rejected"
        ],

        "Interview Scheduled": [
            "Selected",
            "Rejected"
        ],

        "Selected": [],

        "Rejected": []
    }

    if new_status not in valid_transitions[
        application.status
    ]:

        return Response(
            {
                "error": "Invalid status transition."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    application.status = new_status

    application.save()

    return Response(
        {
            "message": "Application status updated successfully.",
            "status": application.status,
            "updated_at": application.updated_at
        }
    )
class EmployerJobListAPIView(ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    serializer_class = JobSerializer

    def get_queryset(self):

        employer = Employer.objects.get(
            user=self.request.user
        )

        return Job.objects.select_related(
            'employer'
        ).filter(
            employer=employer
        )

class ApplicantListAPIView(ListAPIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    serializer_class = ApplicationSerializer

    filter_backends = [
        SearchFilter
    ]

    search_fields = [
        "candidate__full_name"
    ]

    def get_queryset(self):

        employer = Employer.objects.get(
            user=self.request.user
        )

        job = Job.objects.get(
            id=self.kwargs["job_id"]
        )

        # Check job ownership
        if job.employer != employer:

            raise PermissionDenied(
                "Permission denied."
            )

        queryset = Application.objects.select_related(
            "candidate",
            "job"
        ).filter(
            job=job
        )

        print("Before filter:", queryset.count())

        status = self.request.query_params.get(
            "status"
        )

        print("Status received:", status)

        if status:

            queryset = queryset.filter(
                status=status
            )

        print("After filter:", queryset.count())

        return queryset
class EmployerDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def get(self, request):

        employer = Employer.objects.get(
            user=request.user
        )

        jobs = Job.objects.filter(
            employer=employer
        )

        total_jobs = jobs.count()

        active_jobs = jobs.filter(
            is_active=True
        ).count()

        total_applications = Application.objects.filter(
            job__employer=employer
        ).count()

        shortlisted_candidates = Application.objects.filter(
            job__employer=employer,
            status="Shortlisted"
        ).count()

        return Response(
            {
                "total_jobs": total_jobs,
                "active_jobs": active_jobs,
                "total_applications": total_applications,
                "shortlisted_candidates": shortlisted_candidates
            }
        )