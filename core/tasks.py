from celery import shared_task

import time


@shared_task
def send_email_task():

    print("Email sending started...")

    time.sleep(5)

    print("Email sent successfully!")

    return "Success"