from django.contrib.auth import views
from django.urls import path, reverse_lazy

import authentication.views
from . import views as auth_views

app_name = "auth"
urlpatterns = [
    path("login/", authentication.views.combined_login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path("registration/", auth_views.signup, name="registration"),
    path(
        "success-registration/",
        auth_views.success_register,
        name="success-registration",
    ),
    path(
        "success-activation/",
        auth_views.success_activation,
        name="success-activation",
    ),
    path(
        "password_change/", views.PasswordChangeView.as_view(success_url = reverse_lazy("auth:password_change_done")), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(success_url=reverse_lazy('auth:password_reset_done')),
         name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(success_url = reverse_lazy("auth:password_reset_complete")),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
