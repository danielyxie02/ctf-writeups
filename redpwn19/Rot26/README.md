## Rot26
**Category:** pwn  
**Points:** 50

## TLDR
in ```main```:
```
...
  printf(sanitized);
  exit(EXIT_FAILURE);
...
```
Standard format string challenge. Overwrite the lower 2 bytes of ```exit```'s GOT with the lower 2 bytes of ```winners_room``` to spawn a shell and get the flag.

## Writeup
Analyzing the source code, we see a function ```winners_room``` that will give us a shell. Our goal is to redirect code execution here.
Looking in main, we see a vulnerable ```printf``` call, followed by ```exit```:
```
...
  printf(sanitized);
  exit(EXIT_FAILURE);
...
```
So, our attack plan is now clear: use the vulnerable printf to overwrite ```exit```'s Global Offset Table with ```winners_room```'s address, so that when ```exit``` is supposed to be called, ```winners_room``` is called instead.  
Fiddling around with stack offsets, we see that out input begins at the 7th element of the stack (i.e. we control the 7th element of the stack).
```
%x %x %x %x %x %x %x %x %x %x %x 
ffcf693c 1000 8048791 0 0 0 25207825 78252078 20782520 25207825 78252078
...
AAAA%7$x
AAAA41414141
```
Using gdb, we can see that ```exit```'s GOT is ```0x804a020```, and the address of ```winners_room``` is ```0x8048737```.
Lucky for us, the top two bytes are the same, so we only have to overwrite the bottom two bytes (via the ```hn``` option of printf).


