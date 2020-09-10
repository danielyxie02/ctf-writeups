## Zipline
**Category:** pwn  
**Points:** 50

## Writeup
Opening up the binary in IDA, we can observe a few things:
- ```zipline``` is called first, which includes a ```gets``` call. This is a clear indication of something ROP-related.
- ```i_got_u``` is called next, which checks variables ```a```,```b```,```c```, ...```h``` are 0. If any of them are 0, the program doesn't give us the flag. If all the checks pass, we get the flag.
- functions ```air```, ```water```, ```land```, ... ```bedrock``` set variables ```a``` to ```h``` to 1. 

The attack plan is clear: use the ```gets``` call in ```zipline``` to return into each of the functions that set appropriate variables to 1.

(it was also possible to do this challenge by ROPping to ```gets``` and then writing the memory of ```a``` to ```h```)
