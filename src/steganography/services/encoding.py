import uuid

from PIL import Image

from steganography.services.algorithm import SteganographyMethod, data_preparing, bits_to_text
from steganography.services.hadamard import decode_full_message


def encode_image(uploaded_photo, message):
    img = Image.open(uploaded_photo)
    img = img.convert("YCbCr")
    algo = SteganographyMethod()
    w, h = img.size
    message = f"{len(message)}{message}"
    encoded_message_data = data_preparing(message, w, h)
    image = algo.hide_text(img, encoded_message_data)
    name = f"media/processed_photos/encoded_{uuid.uuid4()}.jpg"
    image.save(name, format='JPEG', subsampling=0, quality=100)
    return name


def decode_image(uploaded_photo):
    algo = SteganographyMethod()
    decoded_data = algo.decode_image(uploaded_photo)
    final_message = decode_full_message(decoded_data)
    data = bits_to_text(final_message)
    length = ''
    for l in data[:10]:
        if l.isnumeric():
            length += l
    data = data[len(length):int(length) + len(length)]
    print(data)
    return data

