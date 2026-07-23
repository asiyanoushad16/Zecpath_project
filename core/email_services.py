from django.core.mail import send_mail
from django.conf import settings


def send_reminder_email(interview):

    application = interview.application
    candidate = application.candidate

    send_mail(
        subject="Interview Reminder",
        message=f"""
Hello {candidate.full_name},

This is a reminder for your upcoming interview.

Interview Date : {interview.interview_date}
Interview Time : {interview.interview_time}

Meeting Link:
{interview.meeting_link}

Please join on time.

Best Regards,
HR Team
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[candidate.user.email],
        fail_silently=False,
    )
    print("Email sent successfully!")