# accounts/middleware.py

from zoneinfo import ZoneInfo, available_timezones
from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('user_timezone')
        if tzname in available_timezones():
            timezone.activate(ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
