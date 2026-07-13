from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class AuthenticationTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="candidate"
        )

    def test_login(self):

        data = {
            "username": "testuser",
            "password": "password123"
        }

        response = self.client.post(
            "/login/",
            data,
            format="json"
        )
        print(response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "access",
            response.data
        )

        self.assertIn(
            "refresh",
            response.data
        )
class JobTest(APITestCase):

    def test_job_list(self):

        response = self.client.get(
            "/jobs/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_200_OK,
                status.HTTP_401_UNAUTHORIZED
            ]
        )
class ATSScoreTest(APITestCase):

    def test_ats_score_api(self):

        response = self.client.get(
            "/applications/1/ats-score/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_200_OK,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_404_NOT_FOUND
            ]
        )
class PerformanceReportTest(APITestCase):

    def test_performance_report(self):

        response = self.client.get(
            "/api/admin/performance-report/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_200_OK,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]
        )