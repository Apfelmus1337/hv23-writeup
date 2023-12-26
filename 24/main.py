from PIL import Image, ImageOps
import numpy as np
from pyzbar.pyzbar import decode
import time
from typing import Optional

def check_qr_from_bytes(qr_data: bytes) -> Optional[str]:
    bin_str = ''.join(f'{byte:08b}' for byte in qr_data)[:116*8]

    width, height = 32, 29

    image_data_resized = np.full((height, width), 255, dtype=np.uint8)

    for i, bit in enumerate(bin_str):
        if bit == '1':
            image_data_resized[i // width, i % width] = 0

    out = Image.fromarray(image_data_resized, 'L')
    out = ImageOps.expand(out, border=1, fill=255)
    return decode(out)

def save_qr_from_bytes(name: int, qr_data: bytes):
    bin_str = ''.join(f'{byte:08b}' for byte in qr_data)[:116*8]

    width, height = 32, 29

    image_data_resized = np.full((height, width), 255, dtype=np.uint8)

    for i, bit in enumerate(bin_str):
        if bit == '1':
            image_data_resized[i // width, i % width] = 0

    out = Image.fromarray(image_data_resized, 'L')
    out = ImageOps.expand(out, border=1, fill=255)
    out = out.resize((width * 16, height * 16), Image.BOX)
    out.save(f'out/{name}.png')

def shuffle(qr_data: bytes, D4: int, D5: int, D0: int, D6: int) -> bytes:
    QR_CODE = list(qr_data)
    QR_CODE_END = 112
    sVar5 = D4 - 1

    while sVar5 >= 0:
        if D5 == 0:
            if D0 != -1:
                sVar4 = 28
                index = QR_CODE_END + D0
                uVar1 = QR_CODE[index]
                while sVar4 >= 0:
                    QR_CODE[index] = QR_CODE[index - 4]
                    index -= 4
                    sVar4 -= 1
                QR_CODE[index + 4] = uVar1

            if D6 != -1:
                sVar4 = 3
                index = D6 * 4
                uVar1 = QR_CODE[index]
                while sVar4 >= 0:
                    QR_CODE[index] = QR_CODE[index + 1]
                    sVar4 -= 1
                    index += 1
                QR_CODE[index - 1] = uVar1

        elif D5 == 1:
            if D6 != -1:
                sVar4 = 3
                index = D6 * 4 + sVar4
                uVar1 = QR_CODE[index]
                while sVar4 >= 0:
                    QR_CODE[index] = QR_CODE[index - 1]
                    index -= 1
                    sVar4 -= 1
                QR_CODE[index + 1] = uVar1

            if D0 != -1:
                sVar4 = 28
                index = D0
                uVar1 = QR_CODE[index]
                while sVar4 >= 0:
                    QR_CODE[index] = QR_CODE[index + 4]
                    index += 4
                    sVar4 -= 1
                QR_CODE[index - 4] = uVar1

        sVar5 -= 1

    return bytes(QR_CODE)

if __name__ == '__main__':
    start = time.perf_counter()

    qr_data = open('qr_bytes.txt', 'rb').read()
    scrambles = open('scrambles.txt', 'rb').read()

    cur_shuffled = qr_data
    total_iterations = 10_000

    for i in range(total_iterations):
        for j in range(0, 96, 4):
            cur_scramble = scrambles[j:j+4]
            D6 = cur_scramble[0]
            D0 = cur_scramble[1]
            D4 = cur_scramble[2]
            D5 = cur_scramble[3]
            D6 = -1 if D6 == 0xff else D6
            D0 = -1 if D0 == 0xff else D0
            D4 = -1 if D4 == 0xff else D4
            D5 = -1 if D5 == 0xff else D5

            cur_shuffled = shuffle(cur_shuffled, D4, D5, D0, D6)

        qr = check_qr_from_bytes(cur_shuffled)
        if qr:
            print(f"[+] Index: {i}")
            print(f"[+] Flag: {qr}")
            print(f"[+] Time Taken: {time.perf_counter() - start:02f}s")
            save_qr_from_bytes(i, cur_shuffled)