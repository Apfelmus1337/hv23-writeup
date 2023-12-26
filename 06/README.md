# [HV23.06] Santa should use a password manager

## Introduction

Difficulty: Easy<br>
Author: wangibangi

Santa is getting old and has troubles remembering his password. He said password Managers are too complicated for him and he found a better way. So he screenshotted his password and decided to store it somewhere handy, where he can always find it and where its easy to access.

## Solution

We are given a memory dump where we first scan for all files in the memory:

`py vol.py -f memory.raw windows.filescan.FileScan` 

Now we dump the wallpaper as stated in the description using:

`py vol.py -f memory.raw -o dump/ windows.dumpfiles ‑‑virtaddr 0x918b760e8750`

We get the following picture:

![Fancy Wallpaper](wallpaper.png)

Now all we have to do is scan the QR code for the flag

Flag: `HV23{FANCY-W4LLP4p3r}`