# [HV23.06] Santa should use a password manager

We are given a memory dump where we first scan for all files in the memory:

`py vol.py -f memory.raw windows.filescan.FileScan` 

Now we dump the wallpaper as stated in the description using:

`py vol.py -f memory.raw -o dump/ windows.dumpfiles ‑‑virtaddr 0x918b760e8750`

We get the following picture:

![Fancy Wallpaper](wallpaper.png)

Now all we have to do is scan the QR code for the flag

Flag: `HV23{FANCY-W4LLP4p3r}`
