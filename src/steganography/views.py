import base64
import io
import os
import zipfile
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from django.core.files.storage import default_storage

from core import settings
from steganography.forms import EncryptionForm, DecryptionForm
from steganography.services.encoding import encode_image, decode_image


def home(request):
    return render(request, "steganography/home.html")


def privacy(request):
    return render(request, "steganography/privacy.html")

@login_required
def encoding(request):
    if request.method == "POST":
        form = EncryptionForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.cleaned_data["photo"]
            message = form.cleaned_data["message"]
            processed_photo_url = encode_image(uploaded_photo, message)
            return render(request, "steganography/encoding.html", {
                "form": form,
                "photo_data": processed_photo_url,
            })
        else:
            return render(request, 'steganography/encoding.html', {'form': form})
    else:
        form = EncryptionForm()
        return render(request, "steganography/encoding.html", {
            "form": form,
            "photo_data": None
        })


def save_photo(request):
    if request.method == "POST":
        action = request.POST.get("action")
        photo_url = request.POST.get("photo_data")

        if action == "save":
            if photo_url:
                with open(photo_url, 'rb') as img_file:
                    img_data = img_file.read()
                response = HttpResponse(img_data, content_type="image/jpeg")
                response["Content-Disposition"] = "attachment; filename=processed_photo.jpg"
                return response
        elif action == "email":
            photo_url = request.POST.get("photo_data")
            if photo_url:
                with open(photo_url, 'rb') as img_file:
                    img_data = img_file.read()
                email = EmailMessage(
                    "Processed Photo",
                    "Please find the processed photo attached.",
                    "admin@gmail.com",
                    [request.user.email],
                )
                email.attach("processed_photo.jpg", img_data, "image/jpeg")
                email.send()
                return HttpResponse("Photo sent successfully via email.")
        elif action == "zip":
            photo_url = request.POST.get("photo_data")
            if photo_url:
                with open(photo_url, 'rb') as img_file:
                    img_data = img_file.read()
                zip_buffer = BytesIO()
                with zipfile.ZipFile(
                        zip_buffer, "w", zipfile.ZIP_DEFLATED
                ) as zip_file:
                    zip_file.writestr("processed_photo.jpg", img_data)
                zip_buffer.seek(0)
                response = HttpResponse(
                    zip_buffer.read(), content_type="application/zip"
                )
                response["Content-Disposition"] = (
                    "attachment; filename=processed_photo.zip"
                )
                return response
    return HttpResponse("Invalid action or no data provided.")


@login_required
def decoding(request):
    processed_text = None
    if request.method == "POST":
        form = DecryptionForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.cleaned_data["photo"]
            processed_text = decode_image(uploaded_photo)
            return render(
                request,
                "steganography/decoding.html",
                {
                    "form": form,
                    "processed_text": processed_text,
                },
            )
    else:
        form = DecryptionForm()
        return render(
            request,
            "steganography/decoding.html",
            {"form": form, "processed_text": processed_text},
        )
