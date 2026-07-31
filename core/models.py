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
    choices=ROLE_CHOICES,
    db_index=True
)

    is_verified = models.BooleanField(
    default=False,
    db_index=True
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
    default=False,
    db_index=True
)


    is_active = models.BooleanField(
    default=True,
    db_index=True
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
    default=0,
    db_index=True
)

    expected_salary = models.IntegerField()

    is_active = models.BooleanField(
    default=True,
    db_index=True
)

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name


from django.db import models


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Internship", "Internship"),
    ]

    employer = models.ForeignKey(
        "Employer",
        on_delete=models.CASCADE,
        related_name="jobs"
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
        max_length=100,
        db_index=True
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    featured = models.BooleanField(
        default=False,
        db_index=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
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

    CALL_STATUS_CHOICES = [
        ('Queued', 'Queued'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        db_index=True
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        db_index=True
    )

    resume_snapshot = models.FileField(
        upload_to='application_resumes/',
        blank=True,
        null=True
    )

    ats_score = models.FloatField(
        default=0,
        db_index=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Applied",
        db_index=True
    )


    candidate_available = models.BooleanField(
        default=True
    )

    ai_call_status = models.CharField(
        max_length=20,
        choices=CALL_STATUS_CHOICES,
        default="Queued"
    )

    
    call_scheduled_at = models.DateTimeField(
        null=True,
        blank=True
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
    on_delete=models.CASCADE,
    db_index=True
)

    job = models.ForeignKey(
    Job,
    on_delete=models.CASCADE,
    db_index=True
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
    related_name="timeline",
    db_index=True
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
    on_delete=models.CASCADE,
    db_index=True
)

    action = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.admin.username} - {self.action}"
class AIInterviewSession(models.Model):

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interview_sessions"
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled"
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    transcript = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Session {self.id} - {self.candidate.full_name}"


class AIQuestion(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    asked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question


class AIAnswer(models.Model):

    question = models.ForeignKey(
        AIQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    answer = models.TextField()

    confidence = models.FloatField(default=0)

    relevance_score = models.FloatField(default=0)

    completeness_score = models.FloatField(default=0)

    keyword_score = models.FloatField(default=0)

    final_score = models.FloatField(default=0)

    feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class CallLog(models.Model):

    ACTION_CHOICES = [
        ("Triggered", "Triggered"),
        ("Started", "Started"),
        ("Question Asked", "Question Asked"),
        ("Answer Received", "Answer Received"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    triggered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.action} - Session {self.session.id}"
class QuestionTemplate(models.Model):

    CATEGORY_CHOICES = [
        ("Introduction", "Introduction"),
        ("Experience", "Experience"),
        ("Skills", "Skills"),
        ("Availability", "Availability"),
        ("Salary", "Salary"),
    ]

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    question = models.TextField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question
class JobQuestionMapping(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="question_mappings"
    )

    question = models.ForeignKey(
        QuestionTemplate,
        on_delete=models.CASCADE
    )

    order = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.job.title} - {self.question.question}"
from django.db import models

class InterviewSchedule(models.Model):

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Rescheduled", "Rescheduled"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE
    )

    interviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled"
    )

    meeting_link = models.URLField(
        blank=True,
        null=True
    )


class AvailabilitySlot(models.Model):

    interviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)
class ReminderLog(models.Model):

    interview = models.ForeignKey(
        InterviewSchedule,
        on_delete=models.CASCADE
    )

    sent_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20)

    message = models.TextField(blank=True)
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('PRO', 'Pro'),
        ('ENTERPRISE', 'Enterprise'),
    ]

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    max_job_posts = models.PositiveIntegerField()
    ai_analytics = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class PaymentTransaction(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class BillingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number