import numpy as np


def hadamard_order_n(n):
    if n == 1:
        return np.array([[1]])
    else:
        h_n_minus_1 = hadamard_order_n(n // 2)
        top = np.hstack((h_n_minus_1, h_n_minus_1))
        bottom = np.hstack((h_n_minus_1, -h_n_minus_1))
        return np.vstack((top, bottom))


def encode_message_segment(segment, h):
    index = int(''.join(str(bit) for bit in segment), 2)
    return h[index]


def decode_message_segment(received_bits, h):
    if len(received_bits) == 256:
        distances = np.sum(np.abs(h - received_bits), axis=1)
        index = np.argmin(distances)
        return np.binary_repr(index, width=int(np.log2(len(h))))


def encode_full_message(message, n):
    h = hadamard_order_n(n)
    segment_size = int(np.log2(n))
    encoded_message = []
    for i in range(0, len(message), segment_size):
        segment = message[i:i + segment_size]
        if len(segment) < segment_size:
            segment += [0] * (segment_size - len(segment))
        encoded_message.extend(encode_message_segment(segment, h).tolist())
    return encoded_message


def decode_full_message(encoded_message):
    n = 256
    h = hadamard_order_n(n)
    decoded_bits = []
    for i in range(0, len(encoded_message), n):
        segment = encoded_message[i:i + n]
        decoded_segment = decode_message_segment(segment, h)
        if decoded_segment is not None:
            decoded_bits.append(decoded_segment)
    return ''.join(decoded_bits)
