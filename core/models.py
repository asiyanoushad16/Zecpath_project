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

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
    ]

    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(
        max_length=100,
        db_index=True
    )

    description = models.TextField()

    skills = models.TextField()

    experience = models.IntegerField()

    salary = models.IntegerField()

    location = models.CharField(
        max_length=100
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    featured = models.BooleanField(
    default=False
    )
    
    is_active = models.BooleanField(
        default=True
    )
    
  

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

class Application(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    resume_snapshot = models.FileField(
        upload_to='application_resumes/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,         
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.candidate} - {self.job}"
class SavedJob(models.Model):

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = [
            "candidate",
            "job"
        ]

    def __str__(self):

        return f"{self.candidate} - {self.job}"
class ApplicationTimeline(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="timeline"
    )

    status = models.CharField(
        max_length=30,
        choices=Application.STATUS_CHOICES
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.application} - {self.status}"
class AdminAuditLog(models.Model):

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.admin.username} - {self.action}"