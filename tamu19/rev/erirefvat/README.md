# ReversingErirefvat
## Static analysis
rb() is literally rot13()
ra(char foo) returns rot13(foo) if foo is a letter, and returns foo if it is not a letter.

LBB3_4 is a loop (```for i in range(6)```) getting characters from [rbp-61], applying rot13 (more specifically, calling ra() with the current char), and writing to [rbp-66].

I got frustrated trying to figure out what the first main() loop was and had no clue what app() does at all, so I decided to try using dynamic analysis instead.

The .S has to be compilable by gcc, so I modified some tags and changed some function calls to get it to run.

## Dynamic analysis
As mentioned before, the LBB3_4 writes ra(some character), so to see what's being written we can set a breakpoint right after ra() and examine rax after.

We see that what's being written is 'u', then 'v', then 'c', and gigem{uvc} happens to be the flag.
