# [HV23.14] Crypto Dump

## Introduction

Difficulty: Medium<br>
Author: LogicalOverflow

To keep today's flag save, Santa encrypted it, but now the elf cannot figure out how to decrypt it. The tool just crashes all the time. Can you still recover the flag?

## Solution

## Introduction

Difficulty: Medium<br>
Author: LogicalOverflow

To keep today's flag save, Santa encrypted it, but now the elf cannot figure out how to decrypt it. The tool just crashes all the time. Can you still recover the flag?

## Solution

We are given two files, a binary and a `.zst` file, which turns out to be a coredump, after analyzing it with `gdb` and the binary statically using IDA, I found out the offsets of the Ciphertext, Key and IV inside the coredump, which can be extracted using `gdb`.

```gdb
x/27xb $r13+16 # Ciphertext
0x7fc80c16f050: 0xbd    0x98    0xa7    0x0f    0xfd    0x3a    0x45    0x58
0x7fc80c16f058: 0x18    0x8f    0x8d    0x8e    0xf8    0xbb    0x15    0x66
0x7fc80c16f060: 0x73    0x5f    0x0b    0x61    0x81    0x35    0xbe    0xb5
0x7fc80c16f068: 0x0d    0x80    0xc9
Ciphertext = bd 98 a7 0f fd 3a 45 58 18 8f 8d 8e f8 bb 15 66 73 5f 0b 61 81 35 be b5 0d 80 c9

x/32xb $r15 # Key
0x7ffeef3dd670: 0x9b    0xaf    0x7d    0x5c    0xac    0x41    0x41    0xc8
0x7ffeef3dd678: 0xcb    0x8c    0xfa    0x3f    0xd2    0x70    0xfc    0x4b
0x7ffeef3dd680: 0xee    0xa0    0xcd    0x54    0x0a    0x54    0x25    0x0a
0x7ffeef3dd688: 0xd8    0x8f    0x8f    0x94    0xcb    0x40    0x0f    0x91
Key = 9b af 7d 5c ac 41 41 c8 cb 8c fa 3f d2 70 fc 4b ee a0 cd 54 0a 54 25 0a d8 8f 8f 94 cb 40 0f 91

x/32xb $r13 # IV
0x7fc80c16f040: 0xaf    0x71    0x38    0xad    0x96    0x08    0xc9    0x14
0x7fc80c16f048: 0xbe    0xbd    0xfe    0x19    0xbe    0x9f    0x28    0x25
0x7fc80c16f050: 0xbd    0x98    0xa7    0x0f    0xfd    0x3a    0x45    0x58
0x7fc80c16f058: 0x18    0x8f    0x8d    0x8e    0xf8    0xbb    0x15    0x66
IV = af 71 38 ad 96 08 c9 14 be bd fe 19 be 9f 28 25 bd 98 a7 0f fd 3a 45 58 18 8f 8d 8e f8 bb 15 66
```

After inputting those values into [CyberChef](https://gchq.github.io/CyberChef/#recipe=AES_Decrypt(%7B'option':'Hex','string':'9b%20af%207d%205c%20ac%2041%2041%20c8%20cb%208c%20fa%203f%20d2%2070%20fc%204b%20ee%20a0%20cd%2054%200a%2054%2025%200a%20d8%208f%208f%2094%20cb%2040%200f%2091'%7D,%7B'option':'Hex','string':'af%2071%2038%20ad%2096%2008%20c9%2014%20be%20bd%20fe%2019%20be%209f%2028%2025%20bd%2098%20a7%200f%20fd%203a%2045%2058%2018%208f%208d%208e%20f8%20bb%2015%2066'%7D,'CTR','Hex','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=YmQgOTggYTcgMGYgZmQgM2EgNDUgNTggMTggOGYgOGQgOGUgZjggYmIgMTUgNjYgNzMgNWYgMGIgNjEgODEgMzUgYmUgYjUgMGQgODAgYzk) we are rewarded with the flag.

Flag: `HV23{17's_4ll_ri6h7_7h3r3}`