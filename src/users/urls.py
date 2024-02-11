from django.urls import path

from authentication import views

app_name = "user"

urlpatterns = [
    path(
        "activate/<str:activation_key>/", views.activate_user, name="activate"
    ),
    path(
        "activation_key_not_found/",
        views.activation_key_not_found,
        name="activation_key_not_found",
    ),
    path("user_not_found/", views.user_not_found, name="user_not_found"),
]
