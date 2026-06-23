from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    ]

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


class Employer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=100
    )

    domain = models.CharField(
        max_length=100
    )

    company_size = models.IntegerField()

    verified = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.company_name

class Candidate(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=100
    )

    skills = models.TextField()

    education = models.CharField(
        max_length=100
    )

    experience = models.IntegerField(
        default=0
    )

    expected_salary = models.IntegerField()

    is_active = models.BooleanField(
        default=True
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name


class Job(models.Model):
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.title


class Application(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50,
        default='Applied'
    )

    def __str__(self):
        return f"{self.candidate} - {self.job}"