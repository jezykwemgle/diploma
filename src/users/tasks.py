# from celery import shared_task
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags


def send_activation_email(user, activation_key):
    path_to_act = reverse_lazy(
        "user:activate",
        kwargs={"activation_key": activation_key.key},
    )
    subject = 'Activate Your Account'
    from_email = "admin@admin.com"
    to_email = [user.email]
    context = {
        'user': user,
        'activation_url': f"http://127.0.0.1:8000{path_to_act}"
    }
    html_message = render_to_string('emails/activation.html', context)
    plain_message = strip_tags(html_message)
    send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=to_email,
            fail_silently=False,
        )


def send_response_email(user):
    subject = 'Your Account Has Been Activated'
    from_email = "admin@admin.com"
    to_email = [user.email]
    context = {'user': user}
    html_message = render_to_string('emails/success.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message, fail_silently=False)


def send_confirmation_code_email(user, confirmation_code):
    subject = 'Your Confirmation Code'
    from_email = "admin@admin.com"
    to_email = [user.email]
    context = {
        'user': user,
        'confirmation_code': confirmation_code
    }
    html_message = render_to_string('emails/confirm.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message, fail_silently=False)