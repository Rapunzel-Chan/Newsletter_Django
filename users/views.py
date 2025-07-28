import secrets

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View, ListView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail

from .models import User
from .forms import UserRegisterForm
from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:email_sent")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token  # Обязательно сохранить токен
        user.save()

        url = self.request.build_absolute_uri(reverse("users:email_verification", kwargs={"token": token}))

        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для активации: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return render(self.request, "users/email_verification_notice.html")


class EmailVerificationView(View):
    def get(self, request, token):
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.token = None
        user.save()
        return redirect("users:login")


from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = "users/login.html"


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("users:login")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


@permission_required("auth.change_user", raise_exception=True)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.warning(request, f"Пользователь {user.email} был заблокирован.")
    return redirect("users:users_list")


from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model


@permission_required("users.can_deactivate_user", raise_exception=True)
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.warning(request, f"Пользователь {user.email} был заблокирован.")
    return redirect("users:users_list")
