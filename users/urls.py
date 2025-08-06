from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import (CustomLoginView, CustomLogoutView, EmailVerificationView, UserCreateView,
                         UserDetailView, UserListView, UserPasswordResetCompleteView, UserPasswordResetConfirmView,
                         UserPasswordResetDoneView, UserPasswordResetView, UserProfileUpdateView, deactivate_user)

app_name = UsersConfig.name

urlpatterns = [
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("login/", CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("logout/done/", TemplateView.as_view(template_name="users/logout.html"), name="logout_done"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email_verification/<str:token>/", EmailVerificationView.as_view(), name="email_verification"),
    path(
        "password_reset/",
        UserPasswordResetView.as_view(
            template_name="users/password_reset_form.html", email_template_name="users/password_reset_password.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        UserPasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        UserPasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("<int:user_id>/deactivate/", deactivate_user, name="deactivate_user"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="profile_edit"),
]
