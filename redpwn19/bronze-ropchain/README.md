## Bronze Ropchain
```Category:``` pwn
```Points:``` 50

## Writeup
As the name suggests, it's a ROP chain, as indicated by the blatant ```gets``` call.  
You could try to do this by hand, or you could let [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) do the work for you.  
When using ROPgadget, remember to set a "bad byte" of 0xa; 0xa is a newline which **absolutely cannot** be part of your payload since ```gets``` stops reading at newlines :(


This'll do the trick:
```
ROPgadget --binary ./bronze_ropchain --ropchain --badbytes 0a
```
