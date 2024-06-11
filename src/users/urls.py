from django.urls import path

from authentication import views
from users.views import UserProfileView, UserEditProfileView

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
    path('my-profile/', UserProfileView.as_view(), name='my-profile'),
    path('edit-my-profile/', UserEditProfileView.as_view(), name='edit-my-profile'),
]
