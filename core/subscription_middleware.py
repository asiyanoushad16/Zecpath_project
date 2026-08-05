from django.http import JsonResponse
from django.utils import timezone

from .models import UserSubscription


class SubscriptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            if request.user.role == "employer":

                subscription = UserSubscription.objects.filter(
                    user=request.user,
                    status="ACTIVE",
                    end_date__gte=timezone.now().date()
                ).first()

                if subscription is None:

                    premium_urls = [
                        "/jobs/create/",
                        "/candidate/recommended-jobs/",
                        "/analytics/",
                    ]

                    for url in premium_urls:

                        if request.path.startswith(url):

                            return JsonResponse(
                                {
                                    "message": "Active subscription required."
                                },
                                status=403
                            )

        response = self.get_response(request)

        return response