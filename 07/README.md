# [HV23.07] The golden book of Santa

The website always returns a static image, no matter how we request to it, after looking around for a bit I noticed that it is using `Transfer-Encoding: chunked` for the image it returns, looking at it through `ncat` we can see the individual chunks, where the first chunk is `948`.

This is highly suspicious because `H` is the first character of the flag and `48` in hex, so I wrote a small script to decode the flag.

```py
from pwn import *

docker_url = "d18cb6a1-f874-40c4-9b55-e43e60835713.rdocker.vuln.land"
rem = remote(docker_url, 80)

with open('test.txt', 'wb') as fi:
    rem.sendline("/flag.txt")
    fi.write(rem.recvall())

flag = ""
with open('test.txt', 'r', encoding='utf-8', errors='replace') as fi:
    lines = fi.readlines()

    for line in lines:
        try:
            num = int(line[1:], 16)
            flag += chr(num)
        except:
            pass

print(flag)
```

Flag: `HV23{here_is_your_gift_in_small_pieces}`