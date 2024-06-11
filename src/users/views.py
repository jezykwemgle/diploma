from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from users.models import User


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    """
    Профіль залогіненого юзера.
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserEditProfileView(LoginRequiredMixin, generic.UpdateView):
    """
    Редагування профілю залогіненого юзера.
    """
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = 'users/edit_profile.html'
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse_lazy('user:my-profile')