from django.conf import settings

class SessionCookieSwitcherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If URL contains "adminpanel", use a different session cookie name
        if request.path.startswith('/adminpanel/'):  
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
        else:
            settings.SESSION_COOKIE_NAME = 'client_sessionid'
        return self.get_response(request)
