import random

from django.contrib.auth import get_user_model, logout, authenticate, login
from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from users.models import ActivationKey
from users.tasks import send_activation_email, send_response_email, send_confirmation_code_email
from django import forms

from .forms import RegistrationForm, CombinedLoginForm

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

            send_activation_email(user, activation_key)

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
        send_response_email(user)
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


def generate_and_send_code(user):
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    user.two_factor_code = code
    user.code_sent_time = timezone.now()
    user.save()
    send_confirmation_code_email(user, code)


def verify_two_factor_code(user, code):
    code_valid_duration = 600  # 10 хвилин у секундах
    if user.two_factor_code == code and (timezone.now() - user.code_sent_time).total_seconds() < code_valid_duration:
        return True
    return False


def combined_login_view(request):
    code_sent = False
    form = CombinedLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            two_factor_code = form.cleaned_data.get('two_factor_code', None)
            user = authenticate(username=username, password=password)
            if user and not two_factor_code:
                # Check successful, send code
                generate_and_send_code(user)
                code_sent = True  # Mark that code is sent
                form.fields['username'].initial = username
                form.fields['password'].initial = password
            elif user and two_factor_code:
                # Check 2FA code
                if verify_two_factor_code(user, two_factor_code):
                    login(request, user)
                    return redirect('steganography:home')  # Redirect to home page
                else:
                    form.add_error('two_factor_code', 'Invalid 2FA code')
            else:
                # Authentication failed
                form.add_error(None, 'Invalid username or password')  # Adding a non-field error
        else:
            if 'username' in request.POST:
                form.fields['username'].initial = request.POST['username']
            if 'password' in request.POST:
                form.fields['password'].initial = request.POST['password']
    return render(request, 'registration/login.html', {'form': form, 'code_sent': code_sent})
