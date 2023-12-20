# [HV23.01] A letter from Santa

## Introduction

Difficulty: Easy<br>
Author: coderion

Finally, after 11 months of resting, Santa can finally send out his presents and challenges again. He was writing a letter to his youngest baby elf, who's just learning his **ABC/A-Z**'s. Can you help the elf read the message?

## Solution

The website takes two different types of user input, a character of the alphabet, and then text, after playing around with it for a bit, I started to notice that the character `a` prints the top-most row of a QR-Code, so after writing a short script, we are rewarded with a QR-Code that contains the flag.

```py
import requests

docker_url = "https://fe77bf2d-22cf-4897-9d5f-d2537e6926fa.idocker.vuln.land/"

with open('res.html', 'w') as fi:
    for i in range(26):
        char = chr(97 + i)
        data = {
            'alphabet_select': char,
            'user_input': '| |'
        }

        with requests.post(docker_url, data=data) as resp:
            fi.write(resp.text + '<br>')
```

Flag: `HV23{qr_c0des_fun}`