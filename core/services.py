from .models import Application
import os
import time
from django.conf import settings
from .models import AIQuestion
from .models import JobQuestionMapping



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



class AIBridgeService:

    @staticmethod
    def generate_question(candidate_name):

        try:
            # Replace this with actual LLM API later
            return {
                "success": True,
                "question": f"Hello {candidate_name}, tell me about yourself."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def speech_to_text(audio_file):

        try:
            # Replace with Whisper / Google STT
            return {
                "success": True,
                "text": "Sample speech converted to text."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def text_to_speech(text):

        try:
            # Replace with Google TTS / Azure later
            return {
                "success": True,
                "audio_url": "voice_output.mp3"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def trigger_call(phone):

        try:
            # Replace with Twilio/Exotel later
            return {
                "success": True,
                "message": f"Calling {phone}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class AIBridgeService:

    @staticmethod
    def generate_question(candidate_name):

        try:
            # Replace this with actual LLM API later
            return {
                "success": True,
                "question": f"Hello {candidate_name}, tell me about yourself."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def speech_to_text(audio_file):

        try:
            # Replace with Whisper / Google STT
            return {
                "success": True,
                "text": "Sample speech converted to text."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def text_to_speech(text):

        try:
            # Replace with Google TTS / Azure later
            return {
                "success": True,
                "audio_url": "voice_output.mp3"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def trigger_call(phone):

        try:
            # Replace with Twilio/Exotel later
            return {
                "success": True,
                "message": f"Calling {phone}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }



class QuestionEngineService:

    @staticmethod
    def get_next_question(session):

        mappings = JobQuestionMapping.objects.filter(
            job=session.application.job
        ).order_by("order")

        asked_count = session.questions.count()

        if asked_count >= mappings.count():
            return None

        return mappings[asked_count].question



class AIFlowManager:

    @staticmethod
    def ask_next_question(session):

        question_template = QuestionEngineService.get_next_question(session)

        if question_template is None:

            session.status = "Completed"
            session.save()

            return {
                "message": "Interview Completed"
            }

        question = AIQuestion.objects.create(
            session=session,
            question=question_template.question
        )

        return {
            "question_id": question.id,
            "question": question.question
        }
