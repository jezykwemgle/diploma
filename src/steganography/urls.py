from django.urls import path

from steganography import views

app_name = "steganography"
urlpatterns = [
    path("", views.home, name="home"),
    path("privacy/", views.privacy, name="privacy"),
    path("enc/", views.encoding, name="encoding"),
    path("dec/", views.decoding, name="decoding"),
    path("save_photo/", views.save_photo, name="save_photo"),
]
