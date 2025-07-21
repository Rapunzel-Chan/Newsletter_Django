from django.views.generic import CreateView, View
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail

from .models import User
from .forms import UserRegisterForm
from config.settings import EMAIL_HOST_USER

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:email_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = self.request.build_absolute_uri(
            reverse_lazy('users:email_confirm', kwargs={'uidb64': uid, 'token': token})
        )
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для активации: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return render(self.request, 'users/email_verification_notice.html')


class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.token = ''
            user.save()
            login(request, user)
            return render(request, 'users/activation_success.html')
        return render(request, 'users/activation_invalid.html')


from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('home')


