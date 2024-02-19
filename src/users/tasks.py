# from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse_lazy


# @shared_task
def send_activation_email(email, activation_key):
    path_to_act = reverse_lazy(
        "user:activate",
        kwargs={"activation_key": activation_key.key},
    )
    send_mail(
        subject="User activation",
        message=f"Please activate your account: "
        f"http://127.0.0.1:8000{path_to_act}",
        from_email="admin@admin.com",
        recipient_list=[email],
        fail_silently=False,
    )


# @shared_task
def send_response_email(email):
    send_mail(
        subject="User activation",
        message="User activated successfully.",
        from_email="admin@admin.com",
        recipient_list=[email],
        fail_silently=False,
    )
