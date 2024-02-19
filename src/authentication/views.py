from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from users.models import ActivationKey
from users.tasks import send_activation_email, send_response_email

from .forms import RegistrationForm

User = get_user_model()


def signup(request):
    """
    View to sign up a user. Generate url for activating user account.
    """
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "registration/register.html", {"form": form})
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()
            activation_key = ActivationKey.objects.create(user=user)

            send_activation_email(user.email, activation_key)

            return redirect(reverse_lazy("auth:success-registration"))
        else:
            return render(
                request, "registration/register.html", {"form": form}
            )


def activate_user(request, activation_key):
    """
    View to activate new user`s account and verify their email.
    """
    try:
        activation_obj = ActivationKey.objects.get(key=activation_key)
        user = activation_obj.user
        user.is_active = True
        user.save()
        activation_obj.delete()
        send_response_email(user.email)
        return redirect(reverse_lazy("auth:success-activation"))
    except ActivationKey.DoesNotExist:
        return redirect(reverse_lazy("user:activation_key_not_found"))
    except User.DoesNotExist:
        return redirect(reverse_lazy("user:user_not_found"))


def activation_key_not_found(request):
    """
    View for activation key not found.
    """
    return render(request, "registration/activation_key_not_found.html")


def user_not_found(request):
    """
    View for user not found.
    """
    return render(request, "registration/user_not_found.html")


def success_activation(request):
    """
    View to redirect user to login page.
    """
    return render(request, "registration/success_activation.html")


def success_register(request):
    """ """
    return render(request, "registration/success_register.html")


def logout_view(request):
    """
    View to log out user.
    """
    logout(request)
    return render(request, "registration/logged_out.html")
