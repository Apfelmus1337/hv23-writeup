# [HV23.24] Santa's Shuffled Surprise

## Introduction

Difficulty: 1337<br>
Author: JokerX

Santa found a dusty old floppy disk in his basement. He started the disk in his A500, but the QR code looks shuffled. Can you help him to read the QR code?

## Solution

This was a fun one, retro time with an Amiga 500 Disk Image, I used [FS-UAE](https://fs-uae.net/) to look at the program first. It shows some nice animations and a scrolling text which - after some time reads something along the lines of "click for a QR code", when you click, it switches scenes to a QR code, but some stuff is scrambled.

After inspecting the code in `ghidra` using [ghidra-amiga](https://github.com/BartmanAbyss/ghidra-amiga), I found the following function which I named `scramble24Times`:

```c
undefined4 scramble24Times(void)

{
  undefined4 in_D0;
  short sVar1;
  
  sVar1 = 23;
  do {
    scrambleQR();
    sVar1 = sVar1 + -1;
  } while (sVar1 != -1);
  return in_D0;
}
```

The parameters for `scrambleQR` are not quite right, but they are registers anyway, so I ignored it:

```c
0021f674 7c 00           moveq      #0x0,D6
0021f676 1c 18           move.b     (A0)+=>DAT_0021f5f8,D6b                          = FFh
0021f678 70 00           moveq      #0x0,D0
0021f67a 10 18           move.b     (A0)+=>DAT_0021f5f9,D0b                          = 03h
0021f67c 78 00           moveq      #0x0,D4
0021f67e 18 18           move.b     (A0)+=>DAT_0021f5fa,D4b                          = 01h
0021f680 7a 00           moveq      #0x0,D5
0021f682 1a 18           move.b     (A0)+=>DAT_0021f5fb,D5b                          = 01h
0021f684 b3 45           eor.w      D1w,D5w
0021f686 61 0c           bsr.b      scrambleQR                                       void scrambleQR(void)
```

Here we can see it uses the values starting at `21f5f8`, which is a data block that is exactly `96` bytes long (`24x4`), so we have `24` shuffles/scrambles for our initial QR code.

Shuffles: `ff 03 01 00 0a ff 01 00 0b ff 01 00 ff 01 01 01 0d ff 01 00 0e ff 01 00 ff 01 01 01 ff 02 01 01 11 02 01 00 12 ff 01 00 13 ff 01 00 ff 01 02 01 0e ff 01 00 0a ff 01 00 ff 01 01 00 ff 03 01 00 0d 02 01 00 ff 01 01 00 0f 01 01 01 14 01 01 01 ff 02 01 00 ff 02 01 01 13 ff 01 00 ff 01 01 01`

On top of the QR code being scrambled, it also has a wrong width and height, instead of it being a square its dimensions are `32x29`, which is `928` Pixels, if we take one bit per pixel, that is exactly `116` bytes.

After looking inside `scrambleQR` with `ghidra` we can quickly see the code referencing to `2278c6`, which is the start of our QR-Code segment, that is exactly `118` bytes long. (It seems like it uses 2 bytes as a buffer to not get out of bounds, although I needed 3 buffer bytes in my solve script)

QRCode: `fe a7 f5 70 82 77 3b 40 ba c8 6a 90 ba e3 1a 08 ba c2 ca 70 82 ac 72 e8 fe 0b 2a c0 00 d0 ab 08 fb aa 20 70 e5 88 cd 00 4f aa d2 cd cb 58 b6 d9 8f 10 db f6 2d d5 9b e9 45 69 8b d8 9c c5 68 3f 13 22 e7 0b e9 d9 a8 d8 00 a0 71 84 9e ac 83 f8 a4 f0 08 a0 00 50 ef e8 fe 9e 08 f8 82 ad 9a e8 ba 43 b8 80 ba f9 cf f8 ba b8 ac f0 82 b0 9b 50 fe 2b 29 d0 00 00`

I then started to translate the scrambling code into python, which was very tedious, but worked out well in the end:

ghidra decompile:
```c
void scrambleQR(void)
{
  undefined uVar1;
  undefined1 *puVar2;
  undefined *puVar3;
  int in_D0;
  short sVar4;
  short unaff_D4w;
  short sVar5;
  short unaff_D5w;
  short unaff_D6w;
  undefined *puVar6;
  undefined1 *puVar7;
  
  sVar5 = unaff_D4w + -1;
  do {
    if (unaff_D5w == 0) {
      if ((char)in_D0 != -1) {
        sVar4 = 28;
        uVar1 = (&QR_CODE_END)[in_D0];
        puVar3 = &QR_CODE_END + in_D0;
        do {
          puVar6 = puVar3;
          *puVar6 = puVar6[-4];
          sVar4 = sVar4 + -1;
          puVar3 = puVar6 + -4;
        } while (sVar4 != -1);
        *puVar6 = uVar1;
      }
      sVar4 = 3;
      if ((char)unaff_D6w != -1) {
        uVar1 = (&QR_CODE_START)[unaff_D6w * 4];
        puVar2 = &QR_CODE_START + unaff_D6w * 4;
        do {
          puVar7 = puVar2;
          *puVar7 = puVar7[1];
          sVar4 = sVar4 + -1;
          puVar2 = puVar7 + 1;
        } while (sVar4 != -1);
        *puVar7 = uVar1;
      }
    }
    else {
      if ((char)unaff_D6w != -1) {
        sVar4 = 3;
        uVar1 = (&QR_CODE_INDEX_3)[unaff_D6w * 4];
        puVar3 = &QR_CODE_INDEX_3 + unaff_D6w * 4;
        do {
          puVar6 = puVar3;
          *puVar6 = puVar6[-1];
          sVar4 = sVar4 + -1;
          puVar3 = puVar6 + -1;
        } while (sVar4 != -1);
        *puVar6 = uVar1;
      }
      if ((char)in_D0 != -1) {
        sVar4 = 0x1c;
        uVar1 = (&QR_CODE_START)[in_D0];
        puVar2 = &QR_CODE_START + in_D0;
        do {
          puVar7 = puVar2;
          *puVar7 = puVar7[4];
          sVar4 = sVar4 + -1;
          puVar2 = puVar7 + 4;
        } while (sVar4 != -1);
        *puVar7 = uVar1;
      }
    }
    sVar5 = sVar5 + -1;
  } while (sVar5 != -1);
  return;
}
```

python translation:
```py
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
```

What I did in the end was shuffle the QR Code 24 times 10000 times, until I got a QR Code that was valid and contained the flag:

```py
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
            print(f"[+] Flag: {qr[0].data}")
            print(f"[+] Time Taken: {time.perf_counter() - start:02f}s")
            save_qr_from_bytes(i, cur_shuffled)
```

The correct QR was then found after exactly `4919` shuffles at index `4918`, which funnily enough is `0x1337`.

![flag](./out/4918.png)

Flag: `HV23{J4y_M1n3r_4nd_M17chy_m4d3_17_p0551bl3!!!}`
