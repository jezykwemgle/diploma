import base64
import os
import zipfile
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image

from core import settings
from steganography.forms import EncodingForm
from steganography.services.decoding import decode_image


def home(request):
    return render(request, "steganography/home.html")


def privacy(request):
    return render(request, "steganography/privacy.html")


# @login_required
def encoding(request):
    processed_photo_url = None

    if request.method == "POST":
        form = EncodingForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.cleaned_data["photo"]
            img = Image.open(uploaded_photo)
            img.thumbnail((300, 300))

            # Processing photo with steganography algorithm
            # You need to add your steganography algorithm here

            # Getting URL of processed photo
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            processed_photo_url = "data:image/jpeg;base64," + img_str
            return render(
                request,
                "steganography/encoding.html",
                {
                    "form": form,
                    "processed_photo_url": processed_photo_url,
                    "processed_photo_data": img_str,
                },
            )

    else:
        form = EncodingForm()

    return render(
        request,
        "steganography/encoding.html",
        {"form": form, "processed_photo_url": processed_photo_url},
    )


def save_photo(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "save":
            # Saving processed photo
            photo_data = request.POST.get("photo_data")
            if photo_data:
                img_data = base64.b64decode(
                    photo_data.split(",")[1]
                    if "," in photo_data
                    else photo_data
                )
                with open("processed_photo.jpg", "wb") as f:
                    f.write(img_data)
                with open("processed_photo.jpg", "rb") as f:
                    response = HttpResponse(
                        f.read(), content_type="image/jpeg"
                    )
                    response["Content-Disposition"] = (
                        "attachment; filename=processed_photo.jpg"
                    )
                    return response
        elif action == "email":
            # Sending processed photo via email
            processed_photo_path = os.path.join(
                settings.MEDIA_ROOT, "processed_photo.jpg"
            )
            send_mail(
                "Processed Photo",
                "Please find the processed photo attached.",
                "your@email.com",
                ["recipient@email.com"],
                fail_silently=False,
                html_message="",
                attachment=[
                    (
                        "processed_photo.jpg",
                        open(processed_photo_path, "rb").read(),
                    )
                ],
            )
            return HttpResponse("Photo sent successfully via email.")
        elif action == "zip":
            # Saving processed photo in a zip file
            photo_data = request.POST.get("photo_data")
            if photo_data:
                img_data = base64.b64decode(
                    photo_data.split(",")[1]
                    if "," in photo_data
                    else photo_data
                )
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


@login_required
def decoding(request):
    return render(
        request, "steganography/decoding.html", {"info": decode_image()}
    )
