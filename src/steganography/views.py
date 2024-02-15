from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from steganography.services.decoding import decode_image
from steganography.services.encoding import encode_image


def home(request):
    return render(request, "steganography/home.html")


def privacy(request):
    return render(request, "steganography/privacy.html")


@login_required
def encoding(request):
    return render(
        request, "steganography/encoding.html", {"info": encode_image()}
    )


@login_required
def decoding(request):
    return render(
        request, "steganography/decoding.html", {"info": decode_image()}
    )
