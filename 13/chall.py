#!/usr/bin/python3

import binascii
import io
import subprocess
import zipfile
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
import base64

def hashFile(fileContent:bytes) -> int:
    hash = 0
    for i in range(0, len(fileContent), 8):
        hash ^= sum([fileContent[i+j] << 8*j for j in range(8) if i+j < len(fileContent)])
    return hash

def verifySignature(fileContent:bytes, signatureEncoded:str) -> bool:
    signature = base64.b64decode(signatureEncoded)
    hash = hashFile(fileContent)
    try:
        pkcs1_15.new(KEY).verify(SHA1.new(hex(hash).encode()), signature)
        return True
    except ValueError:
        return False
    
def fileSignature(fileContent:bytes):
    hash = hashFile(fileContent)
    signature = pkcs1_15.new(KEY).sign(SHA1.new(hex(hash).encode()))
    return base64.b64encode(signature)

def verifyAndExtractZipFile(fileContentEncoded:str, signature:str):
    try:
        fileContent = base64.b64decode(fileContentEncoded)
    except binascii.Error:
        print('Invalid Base64 file')
        return
    try:
        if not verifySignature(fileContent, signature):
            print("Signature is invalid")
            return
    except binascii.Error:
        print('Invalid Base64 signature')
        return
    files = zipfile.ZipFile(io.BytesIO(fileContent))
    startFile = [x for x in files.filelist if 'start.sh' in x.filename]
    if len(startFile) == 0:
        print("No start.sh included in the firmware")
        return
    filePath = files.extract(startFile[0], path='./www/root/')
    p = subprocess.Popen(['/bin/sh', filePath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'Update exited with statuscode {p.wait()}')
