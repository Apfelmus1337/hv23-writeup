# [HV23.12] unsanta

## Introduction

Difficulty: Medium<br>
Author: kuyaya

To train his skills in cybersecurity, Grinch has played this year's SHC qualifiers. He was inspired by the cryptography challenge unm0unt41n (can be found [here](https://library.m0unt41n.ch/)) and thought he might play a funny prank on Santa. Grinch is a script kiddie and stole the malware idea and almost the whole code. Instead of using the original encryption malware from the challenge though, he improved it a bit so that no one can recover his secret!

Luckily, Santa had a backup of one of the images. Maybe this can help you find the secret and recover all of Santa's lost data...?

## Solution

Oh boy, this one was painful, first I saw random, I used randcrack, recovered the two other memes, and got made fun of, I don't have it anymore because of my git-typo, but the second meme basically said "I see random, I use randcrack" and the second meme was a RickRoll as per usual.

After some time while trying to solve the challenge I stumbled upon a really similar challenge, where you had to recover the seed of a python random initialization, which led me to the following Git Repo: [RNGeesus](https://github.com/deut-erium/RNGeesus), this library provided a POC to recover a seed from a Mersenne Twister state.

```py
from mersenne import BreakerPy

plaintext = open("unsanta/backup/a.jpg", 'rb').read()
ciphertext = open("unsanta/memes/a.jpg", 'rb').read()

xors = []
for i in range(0, 624*4, 4):
    plain_dec = int.from_bytes(plaintext[i:i+4])
    cipher_dec = int.from_bytes(ciphertext[i:i+4])
    xors.append(plain_dec ^ cipher_dec)

print(b''.join([x.to_bytes(4) for x in BreakerPy().get_seeds_python_fast(xors)][::-1]))
```

Flag: `HV23{s33d_r3c0very_1s_34sy}`