from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Employer, Candidate, Job, Application,AIInterviewSession,AIQuestion,AIAnswer,CallLog,QuestionTemplate,JobQuestionMapping,AvailabilitySlot, InterviewSchedule



@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'phone',
        'role',
        'is_verified',
        'is_active',
    )

    list_filter = (
        'role',
        'is_verified',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom Fields',
            {
                'fields': (
                    'phone',
                    'role',
                    'is_verified',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                'fields': (
                    'email',
                    'phone',
                    'role',
                    'is_verified',
                )
            },
        ),
    )


admin.site.register(Employer)
admin.site.register(Candidate)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(AIInterviewSession)
admin.site.register(AIQuestion)
admin.site.register(AIAnswer)
admin.site.register(CallLog)
admin.site.register(QuestionTemplate)
admin.site.register(JobQuestionMapping)
admin.site.register(AvailabilitySlot)
admin.site.register(InterviewSchedule)