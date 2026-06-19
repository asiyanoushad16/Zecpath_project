from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Employer, Candidate, Job, Application


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