from django.shortcuts import render

from steganography.services.decoding import decode_image
from steganography.services.encoding import encode_image


def home(request):
    return render(request, "steganography/home.html")


def privacy(request):
    return render(request, "steganography/privacy.html")


def encoding(request):
    return render(
        request, "steganography/encoding.html", {"info": encode_image()}
    )


def decoding(request):
    return render(
        request, "steganography/decoding.html", {"info": decode_image()}
    )
