import random

from PIL import Image

from steganography.services.hadamard import encode_full_message, decode_full_message

csi_4 = [1, -1, -1, 1,
         1, -1, -1, 1,
         1, -1, -1, 1,
         1, -1, -1, 1]

csi_4_8x8 = [[1, -1, -1, 1, 1, -1, -1, 1],
             [1, -1, -1, 1, 1, -1, -1, 1],
             [1, -1, -1, 1, 1, -1, -1, 1],
             [1, -1, -1, 1, 1, -1, -1, 1],

             [-1, 1, 1, -1, -1, 1, 1, -1],
             [-1, 1, 1, -1, -1, 1, 1, -1],
             [-1, 1, 1, -1, -1, 1, 1, -1],
             [-1, 1, 1, -1, -1, 1, 1, -1]]


class SteganographyMethod:
    def __init__(self):
        self.T1 = csi_4
        self.T1_8x8 = csi_4_8x8
        self.T2 = csi_4
        self.T2_8x8 = csi_4_8x8

    def hide_text(self, im1, message: list[int]):
        # im1 = Image.open(empty_container)
        # im1 = im1.convert("YCbCr")
        width, height = im1.size

        message_index = 0
        for i in range(0, width, 8):
            for j in range(0, height, 8):
                for l1 in range(8):
                    for l2 in range(8):
                        [y, cb, cr] = im1.getpixel((i + l1, j + l2))
                        if y != 255 and y != 0 and message_index < len(message):
                            if message[message_index] == 1:
                                y += self.T1_8x8[l1][l2] + self.T2_8x8[l1][l2]
                            else:
                                y += ((-1) * self.T1_8x8[l1][l2]) + ((-1) * self.T2_8x8[l1][l2])
                        else:
                            y = y
                        value = (y, cb, cr)
                        im1.putpixel((i + l1, j + l2), value)
                message_index += 1

        # im1.save(encoded_file_name, format='JPEG', subsampling=0, quality=100)
        return im1

    def decode_image(self, full_container):
        full_container = Image.open(full_container)
        im3 = full_container.convert("YCbCr")
        width, height = im3.size

        k = 0
        data = []
        for i in range(0, width, 8):
            for j in range(0, height, 8):
                proxima = 0
                f1 = []
                f2 = []
                f3 = []
                f4 = []
                for l1 in range(4):
                    for l2 in range(4):
                        f1.append(im3.getpixel((i + l1, j + l2)))
                for l1 in range(4):
                    for l2 in range(4):
                        f2.append(im3.getpixel((i + l1, j + 4 + l2)))
                for l1 in range(4):
                    for l2 in range(4):
                        f3.append(im3.getpixel((i + 4 + l1, j + l2)))
                for l1 in range(4):
                    for l2 in range(4):
                        f4.append(im3.getpixel((i + 4 + l1, j + 4 + l2)))

                w11 = 0
                for l1 in range(16):
                    w11 += f1[l1][0] * self.T1[l1]
                w12 = 0
                for l1 in range(16):
                    w12 += f2[l1][0] * self.T1[l1]
                w13 = 0
                for l1 in range(16):
                    w13 += f3[l1][0] * self.T1[l1]
                w14 = 0
                for l1 in range(16):
                    w14 += f4[l1][0] * self.T1[l1]

                w21 = 0
                for l1 in range(16):
                    w21 += f1[l1][0] * self.T2[l1]
                w22 = 0
                for l1 in range(16):
                    w22 += f2[l1][0] * self.T2[l1]
                w23 = 0
                for l1 in range(16):
                    w23 += f3[l1][0] * self.T2[l1]
                w24 = 0
                for l1 in range(16):
                    w24 += f4[l1][0] * self.T2[l1]

                wav1 = (w11 + w12 + w13 + w14) / 4
                wav2 = (w21 + w22 + w23 + w24) / 4

                proxima = ((w11 - wav1) +
                           (w12 - wav1) -
                           (w13 - wav1) -
                           (w14 - wav1) +
                           (w21 - wav2) +
                           (w22 - wav2) -
                           (w23 - wav2) -
                           (w24 - wav2))

                if proxima >= 0:
                    data.append(1)
                else:
                    data.append(-1)
        return data


def bits_to_text(bits):
    # chars = [''.join(bits[i:i + 8]) for i in range(0, len(bits), 8)]
    # text = ''.join(chr(int(char, 2)) for char in chars)
    text = ''
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        char = chr(int(''.join(map(str, byte)), 2))
        text += char
    return text


def text_to_bits(text):
    bits = []
    for char in text:
        char_bits = bin(ord(char))[2:].zfill(8)
        bits.extend(int(bit) for bit in char_bits)
    return bits


def data_preparing(text, width, height):
    """
    Готує повідомлення для внесення в зображення.
    Переводить повідомлення в формат [-1, 1]
    """
    bits = text_to_bits(text)
    encoded_message_data = encode_full_message(bits, 256)

    # additive_info = [(-1) ** random.randrange(2) for _ in range((width * height) // 64 - len(encoded_message_data))]
    # encoded_message_data.extend(additive_info)
    return encoded_message_data


def data_getting(message):
    """Перетворюємо отримане повідомлення з зображення з формату [-1, 1] в текст"""
    bits = decode_full_message(message)
    chars = bits_to_text(bits)
    return chars


# def process_image(input_image_path, output_image_path, message):
#     algo = SteganographyMethod()
#     image = Image.open(input_image_path)
#     w, h = image.size
#
#     encoded_message_data = data_preparing(message, w, h)
#     algo.hide_text(input_image_path, output_image_path, encoded_message_data)
#
#     decoded_data = algo.decode_image(output_image_path)  # list[int] 1/-1
#     final_message = decode_full_message(decoded_data)
#     data = bits_to_text(final_message)[:100]
#     return data
#
#
# if __name__ == '__main__':
#     text = "hello world!"
#     prepared = data_preparing(text, 256, 256)
#     print(prepared)
#
#     result = data_getting(prepared)
#     print(result)
