from django.contrib.auth import views
from django.urls import path

from . import views as auth_views

app_name = "auth"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
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
]
