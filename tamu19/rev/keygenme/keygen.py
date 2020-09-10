def enc(msg):
	res = ""
	cnt = 0
	prev = 'H'
	for i in msg:
		rax = ord(i)
		rdx = ord(i) + 0xc
		rax = ord(prev)*rdx
		rcx = rax + 0x11
		rdx = 0xea0ea0eb
		rax = (rcx * rdx) >> 32
		rax = rax >> 6
		rdx = rax
		rax = rcx
		rax = rax >> 0x1f
		rdx = rdx - rax
		rax = rdx
		rax = rax*0x46
		rcx = rcx - rax
		rax = rcx
		rcx = rax + 0x30
		res += chr(rcx)
		prev = res[cnt]
		cnt += 1
	return res

if __name__ == "__main__":
	target = "[OIonU2_<__nK<KsK"
	found = ""
	for i in range(len(target)-1):
		for test in range(256):
			if enc(found + chr(test)) == target[:i+1] and 33<=test<=126:
				found += chr(test)
				break
	print found