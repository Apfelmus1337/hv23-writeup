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
