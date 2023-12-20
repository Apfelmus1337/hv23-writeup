# [HV23.04] Bowser

## Introduction

Difficulty: Easy<br>
Author: veganjay

Santa has heard that some kids appreciate a video game as a christmas gift. He would rather have the kids solve some CTF challenges, so he took some inspiration and turned it into a challenge. Can you save the princess?

## Solution

This was the first reversing challenge, we are given an executable called bowser, which prints a big ASCII-Art of Bowser, there's also a really simple check for a supplied `argv[1]`, but after supplying `mario`, which should be correct according to BinaryNinja, we are given `Sorry, your flag is in another castle.`

BinaryNinja decompile:
```c
00001323      void* fsbase
00001323      int64_t rax = *(fsbase + 0x28)
00001346      int64_t str
00001346      __builtin_memcpy(dest: &str, src: "\xac\x90\x8d\x8d\x86\xd3\xdf\x86\x90\x8a\x8d\xdf\x99\x93\x9e\x98\xdf\x96\x8c\xdf\x96\x91\xdf\x9e\x91\x90\x8b\x97\x9a\x8d\xdf\x9c\x9e\x8c\x8b\x93\x9a\xd1\xff\xb7\xa9\xcd\xcc\x84\xa6\x90\x8a\xa0\xb7\x9e\x89\x9a\xa0\xac\x9e\x89\x9a\x9b\xa0\x8b\x97\x9a\xa0\xaf\x8d\x96\x91\x9c\x9a\x8c\x8c\x82", n: 0x48)
000013b0      char var_20 = 0
000013b9      bowser()
000013c2      int32_t rax_5
000013c2      if (argc != 2)
000013da          printf(format: "Usage: %s password\n", *argv)
000013df          rax_5 = 1
00001402      else if (strcmp(argv[1], "mario") != 0)
0000140b          puts(str: "Sorry, that is not the correct p…")
00001410          rax_5 = 1
0000141b      else
0000141b          int64_t* var_70_1 = &str
00001440          while (*var_70_1 != 0)
00001430              *var_70_1 = (not.d(zx.d(*var_70_1))).b
00001432              var_70_1 = var_70_1 + 1
00001449          puts(str: &str)
0000144e          rax_5 = 0
00001460      if (rax == *(fsbase + 0x28))
00001468          return rax_5
00001462      __stack_chk_fail()
00001462      noreturn
```

After putting the 0x48 big Byte-Array into CyberChef and applying the `NOT` operator onto it, we get the flag and also see the reason, why it wasn't output by the binary itself, a sneakily placed NULL-byte.

CyberChef Link: [solve](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')NOT()&input=XHhhY1x4OTBceDhkXHg4ZFx4ODZceGQzXHhkZlx4ODZceDkwXHg4YVx4OGRceGRmXHg5OVx4OTNceDllXHg5OFx4ZGZceDk2XHg4Y1x4ZGZceDk2XHg5MVx4ZGZceDllXHg5MVx4OTBceDhiXHg5N1x4OWFceDhkXHhkZlx4OWNceDllXHg4Y1x4OGJceDkzXHg5YVx4ZDFceGZmXHhiN1x4YTlceGNkXHhjY1x4ODRceGE2XHg5MFx4OGFceGEwXHhiN1x4OWVceDg5XHg5YVx4YTBceGFjXHg5ZVx4ODlceDlhXHg5Ylx4YTBceDhiXHg5N1x4OWFceGEwXHhhZlx4OGRceDk2XHg5MVx4OWNceDlhXHg4Y1x4OGNceDgy)

Flag: `HV23{You_Have_Saved_the_Princess}`