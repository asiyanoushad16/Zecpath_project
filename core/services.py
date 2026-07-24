from .models import Application
import os
import time
from django.conf import settings
from .models import AIQuestion
from .models import JobQuestionMapping
from .models import AvailabilitySlot, InterviewSchedule
from .models import AIInterviewSession, AIAnswer
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg


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
class AnswerEvaluationService:

    @staticmethod
    def evaluate(question, answer):

        expected_keywords = [
            "python",
            "django",
            "database",
            "api",
            "orm",
            "sql",
            "authentication",
            "jwt",
            "model",
            "query"
        ]

        answer_lower = answer.lower()

        matched = 0

        for word in expected_keywords:
            if word in answer_lower:
                matched += 1

        keyword_score = (matched / len(expected_keywords)) * 10

        relevance_score = 8 if matched > 2 else 4

        completeness_score = 9 if len(answer.split()) > 20 else 5

        final_score = (
            relevance_score * 0.5 +
            completeness_score * 0.3 +
            keyword_score * 0.2
        )

        feedback = "Excellent Answer"

        if final_score < 5:
            feedback = "Needs Improvement"

        confidence = 95

        return {
            "confidence": confidence,
            "relevance": relevance_score,
            "completeness": completeness_score,
            "keyword": keyword_score,
            "final": round(final_score, 2),
            "feedback": feedback
        }

class SchedulingService:

    @staticmethod
    def schedule_interview(application, interviewer):

        slot = AvailabilitySlot.objects.filter(
            interviewer=interviewer,
            is_booked=False
        ).order_by("date", "start_time").first()

        if not slot:
            return {
                "success": False,
                "message": "No available slots."
            }

        slot.is_booked = True
        slot.save()

        interview = InterviewSchedule.objects.create(
            application=application,
            interviewer=interviewer,
            interview_date=slot.date,
            interview_time=slot.start_time,
            status="Scheduled",
            meeting_link="https://meet.google.com/sample-link"
        )

        
        SchedulingService.send_notification(
            application,
            interview
        )

        return {
            "success": True,
            "message": "Interview Scheduled Successfully",
            "interview_id": interview.id,
            "date": interview.interview_date,
            "time": interview.interview_time
        }

    @staticmethod
    def get_available_slots(interviewer):

        slots = AvailabilitySlot.objects.filter(
            interviewer=interviewer,
            is_booked=False
        ).order_by("date", "start_time")

        return slots

    @staticmethod
    def reschedule_interview(interview, new_slot):

        if new_slot.is_booked:
            return {
                "success": False,
                "message": "Selected slot is already booked."
            }

        old_slot = AvailabilitySlot.objects.get(
            interviewer=interview.interviewer,
            date=interview.interview_date,
            start_time=interview.interview_time
        )

        old_slot.is_booked = False
        old_slot.save()

        new_slot.is_booked = True
        new_slot.save()

        interview.interview_date = new_slot.date
        interview.interview_time = new_slot.start_time
        interview.status = "Rescheduled"
        interview.save()

        return {
            "success": True,
            "message": "Interview Rescheduled Successfully"
        }

    @staticmethod
    def cancel_interview(interview):

        slot = AvailabilitySlot.objects.get(
            interviewer=interview.interviewer,
            date=interview.interview_date,
            start_time=interview.interview_time
        )

        slot.is_booked = False
        slot.save()

        interview.status = "Cancelled"
        interview.save()

        return {
            "success": True,
            "message": "Interview Cancelled Successfully"
        }

    @staticmethod
    def validate_slot(slot):

        if slot.is_booked:
            return False

        return True

    @staticmethod
    def send_notification(application, interview):

        candidate = application.candidate

        send_mail(
            subject="Interview Scheduled",
            message=(
                f"Hello {candidate.full_name},\n\n"
                f"Your interview has been scheduled successfully.\n\n"
                f"Interview Details:\n"
                f"Date: {interview.interview_date}\n"
                f"Time: {interview.interview_time}\n"
                f"Meeting Link: {interview.meeting_link}\n\n"
                f"Best Regards,\n"
                f"HR Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[candidate.user.email],
            fail_silently=False,
        )

        return {
            "success": True,
            "message": "Interview notification sent successfully."
        }



class AIReportService:

    @staticmethod
    def generate_report(application):

        print("=" * 50)
        print("Application ID:", application.id)

        session = AIInterviewSession.objects.filter(
            application=application,
            status="Completed"
        ).last()

        print("Session:", session)

        if not session:
            print("No completed session found.")
            return {
                "success": False,
                "message": "Interview session not completed."
            }

        questions = session.questions.all()

        print("Questions Count:", questions.count())

        for question in questions:
            print("Question ID:", question.id)
            print("Question:", question.question)

        answers = AIAnswer.objects.filter(
            question__session=session
        )

        print("Answers Count:", answers.count())

        for answer in answers:
            print("Answer ID:", answer.id)
            print("Answer:", answer.answer)

        if not answers.exists():
            return {
                "success": False,
                "message": "No interview answers found."
            }

        stats = answers.aggregate(
            avg_confidence=Avg("confidence"),
            avg_relevance=Avg("relevance_score"),
            avg_completeness=Avg("completeness_score"),
            avg_keyword=Avg("keyword_score"),
            avg_final=Avg("final_score"),
        )

        ats_score = application.ats_score
        ai_score = round(stats["avg_final"] or 0, 2)

        strengths = []
        risks = []

        if ats_score >= 80:
            strengths.append("Strong resume match")
        else:
            risks.append("Resume ATS score is below expectation")

        if (stats["avg_keyword"] or 0) >= 7:
            strengths.append("Good technical knowledge")
        else:
            risks.append("Weak technical keyword coverage")

        if (stats["avg_completeness"] or 0) >= 7:
            strengths.append("Provides detailed answers")
        else:
            risks.append("Answers need more detail")

        if (stats["avg_relevance"] or 0) >= 7:
            strengths.append("Answers are relevant")
        else:
            risks.append("Some answers lack relevance")

        if ai_score >= 8:
            recommendation = "Highly Recommended"
        elif ai_score >= 6:
            recommendation = "Recommended"
        else:
            recommendation = "Needs Review"

        summary = (
            f"The candidate achieved an ATS score of {ats_score:.2f} "
            f"and an AI interview score of {ai_score:.2f}. "
            f"Overall Recommendation: {recommendation}."
        )

        print("=" * 50)

        return {
            "candidate": application.candidate.full_name,
            "job": application.job.title,
            "ats_score": ats_score,
            "ai_call_score": ai_score,
            "average_confidence": round(stats["avg_confidence"] or 0, 2),
            "average_relevance": round(stats["avg_relevance"] or 0, 2),
            "average_completeness": round(stats["avg_completeness"] or 0, 2),
            "average_keyword_score": round(stats["avg_keyword"] or 0, 2),
            "strengths": strengths,
            "risks": risks,
            "recommendation": recommendation,
            "summary": summary,
        }