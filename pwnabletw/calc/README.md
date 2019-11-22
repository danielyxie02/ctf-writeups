# calc (150 pts)
> Have you ever use Microsoft calculator?
>
> nc chall.pwnable.tw 10100

## Analysis
An infinite loop in ```calc()``` runs as long as the user is using the calculator. In each pass, the program 
1. Zeroes out a buffer that stores the user-supplied expression as well as well as a buffer that stores the result
2. Gets the expression by calling ```get_expr()```
3. Evaluates the expression by calling ```parse_expr()```
4. Prints the result

1, 2, and 4 are pretty self-explanatory and secure, so there's no need to look deeper into them. 

### Looking closer at ```parse_expr()```
Let's consider a simple expression like "1+1". The function iterates through every character of the expression. When it hits an operation, in this case ```+```, the program stops and does some calculations (don't worry about PEMDAS, it more or less tries its best to cover it). 

todo: some more explanation abt the pool + other stuff, ghidra takes too much battery and im at 11%
#### The ```eval()``` function

This function takes two arguments:
1. A pointer to the pool 
2. The operation it needs to perform

Here's what the function does: 

```pool[pool[0]-1] = pool[pool[0]-1] {operation} pool[pool[0]]```

where the operation is +, -, \*, or /.

This is, of course, based on the assumption that ```pool[0] = 2```, so ```pool[1]``` is the left operand and ```pool[2]``` is the right operand, and that's where the vulnerability is. By entering an expression with no left operand, e.g. ```+10000```, ```pool[0]``` has a value of 1, not 2. As a result, this operation is performed:

```pool[0] = pool[0] {operation} pool[1]```

Since we can enter any number as ```pool[1]```, we have control over ```pool[0]``` by the statement above. Then, control over ```pool[0]``` gives us control over ```pool[n]```, giving us an arbitrary write. 

This vulnerability also gives us a leak, since ```parse_expr``` prints the result of the operation by printing ```pool[0]```. 
