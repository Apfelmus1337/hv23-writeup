from mersenne import BreakerPy

plaintext = open("unsanta/backup/a.jpg", 'rb').read()
ciphertext = open("unsanta/memes/a.jpg", 'rb').read()

xors = []
for i in range(0, 624*4, 4):
    plain_dec = int.from_bytes(plaintext[i:i+4])
    cipher_dec = int.from_bytes(ciphertext[i:i+4])
    xors.append(plain_dec ^ cipher_dec)

print(b''.join([x.to_bytes(4) for x in BreakerPy().get_seeds_python_fast(xors)][::-1]))