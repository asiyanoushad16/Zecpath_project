from celery import shared_task

import time


@shared_task
def send_email_task():

    print("Email sending started...")

    time.sleep(5)

    print("Email sent successfully!")

    return "Success"
from celery import shared_task
from .models import Application


@shared_task
def process_ai_call(application_id):

    application = Application.objects.get(id=application_id)

    # AI Call Started
    application.ai_call_status = "In Progress"
    application.save()

    # Here your AI interview logic will come
    # Example:
    # Speech to Text
    # LLM
    # Text to Speech

    # AI Call Finished
    application.ai_call_status = "Completed"
    application.save()

    return "AI Call Completed"
from celery import shared_task
from .models import Application


@shared_task(bind=True, max_retries=3)
def process_ai_call(self, application_id):

    try:

        application = Application.objects.get(id=application_id)

        application.ai_call_status = "In Progress"
        application.save()

        # AI Interview Logic

        application.ai_call_status = "Completed"
        application.save()

        return "Completed"

    except Exception as exc:

        application.ai_call_status = "Failed"
        application.save()

        raise self.retry(
            exc=exc,
            countdown=30
        )