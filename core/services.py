from .models import Application


class AIEligibilityService:

    @staticmethod
    def check(application):

        if application.ats_score < 60:
            return False

        if application.status != "Shortlisted":
            return False

        if not application.job.is_active:
            return False

        if not application.candidate_available:
            return False

        return True



from datetime import time
from django.utils import timezone
from .tasks import process_ai_call


class AISchedulerService:

    @staticmethod
    def is_business_hours():

        current_time = timezone.localtime().time()

        start = time(9, 0)
        end = time(18, 0)

        return start <= current_time <= end

    @staticmethod
    def schedule_call(application):

        if AISchedulerService.is_business_hours():
            process_ai_call.delay(application.id)
            return "Queued"

        return "Outside Business Hours"

