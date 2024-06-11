import re

from PIL import Image
from django import forms


class EncryptionForm(forms.Form):
    photo = forms.ImageField(label='', required=True)
    message = forms.CharField(label="Tell me your secret", required=True, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        photo = cleaned_data.get('photo')
        message = cleaned_data.get('message')
        if not re.match(r'^[a-zA-Z0-9 .,?!@#$%^&*()_+-=:";\'<>{}[\]\\|`~]*$', message):
            raise forms.ValidationError("The message contains invalid characters.")

        if photo:
            image = Image.open(photo)
            width, height = image.size

            max_bytes = (height * width / 64) / 266
            print(max_bytes)
            if len(message.encode('utf-8')) > max_bytes - 1:
                raise forms.ValidationError(f"The message is too long. It must be at most {int(max_bytes)} bytes.")
        return cleaned_data


class DecryptionForm(forms.Form):
    photo = forms.ImageField(label='', required=True)
