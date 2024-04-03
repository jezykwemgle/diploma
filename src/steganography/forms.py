from django import forms


class EncodingForm(forms.Form):
    photo = forms.ImageField(label="Choose photo")
    message = forms.CharField(label="Текстове повідомлення")
    SAVE_CHOICES = (
        ("save", "Зберегти"),
        ("zip", "Зіп-файл"),
        ("email", "Відправити електронною поштою"),
    )
    save_option = forms.ChoiceField(
        choices=SAVE_CHOICES, widget=forms.RadioSelect
    )
