# [HV23.17] Lost Key

## Introduction

Difficulty: Hard<br>
Author: darkstar

After losing another important key, the administrator sent me a picture of a key as a replacement. But what should I do with it?

![key](key.png)

## Solution

First I ran `exiftool` on the `key.png` file, I saw `e=0x10001`, this clearly hints at RSA.

After spending a literal eternity searching for stuff in the specific bit-planes of the key image I noticed two little dots, one in the middle on the very right side and one in the bottom-right corner, how fun would it be if he only modified the last pixel to get two prime numbers for `p` and `q`?

Well, not fun at all, but in the end the script finished executing, it took quite some time... (around 5 minutes)

```py
from Crypto.Util.number import bytes_to_long, long_to_bytes
from PIL import Image

im = Image.open('key.png')
pq = im.tobytes()
size = len(pq) // 2

p = bytes_to_long(pq[:size])
q = bytes_to_long(pq[size:])

data = open("flag.enc", "rb").read()
ciphertext = bytes_to_long(data)

phi = (p - 1) * (q - 1)
n = p * q
e = 0x10001
d = pow(e, -1, phi)
flag = long_to_bytes(pow(ciphertext, d, n))

with open('flag.png', 'wb') as f: 
    f.write(flag)
```

This gave us a tiny little QR Code, which upon scanning gives us the flag.

![flag](flag.png)

Flag: `HV23{Thanks_for_finding_my_key}`