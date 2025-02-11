from django.urls import reverse
from django.shortcuts import redirect


class RedirectAuthenticatedUserMiddleware:    # بعد از لاگین به این صفحات دسترسی ندارید
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_urls = [
            reverse('account:register'),
            reverse('account:verify_code'),
            reverse('account:login'),
            reverse('account:forget'),
            reverse('account:forget_otp'),
            reverse('account:reset_password'),
            reverse('account:enter_otp'),
            reverse('account:enter_otp_verify'),
        ]

    def __call__(self, request):
        if request.user.is_authenticated and request.path in self.restricted_urls:
            return redirect('BlogApp:home')
        return self.get_response(request)
